"""Lifecycle records for provider and cloud operations.

Each operation is saved as dispatched before the provider is called. After a
crash, a dispatched operation with a saved receipt is recovered as received;
one without a receipt is uncertain and blocks further dispatch of that kind
until a person reconciles it. Counted calls stay counted in every case.

States: dispatched -> received -> committed | invalid; dispatched -> failed;
dispatched -> not_dispatched (the provider process never started);
dispatched -> uncertain -> reconciled_failed | reconciled_received.
"""
import hashlib
import json
import time

from pilot import require

TERMINAL = {'committed', 'invalid', 'failed', 'not_dispatched', 'reconciled_failed', 'reconciled_received'}
REPLAY_BLOCKED = {'received', 'committed', 'invalid', 'reconciled_received'}


def fingerprint(message):
    """Hash of the exact request body."""
    data = message if isinstance(message, bytes) else str(message).encode()
    return hashlib.sha256(data).hexdigest()


def ledger(project):
    """The project's operation records, keyed by logical id."""
    return project.setdefault('operations', {})


def begin(project, op_id, kind, message, role=None, provider=None, call=None):
    """Record intent and dispatch before the provider is called. A completed operation is never replayed."""
    records = ledger(project)
    existing = records.get(op_id)
    require(not existing or existing.get('state') not in REPLAY_BLOCKED,
            'Operation ' + op_id + ' already completed. A completed call is not replayed.')
    require(not existing or existing.get('state') not in {'dispatched', 'uncertain'},
            'Operation ' + op_id + ' was dispatched and has no provider receipt. Reconcile it before another dispatch.')
    attempts = int((existing or {}).get('attempts') or 0) + 1
    records[op_id] = {'id': op_id, 'kind': kind, 'role': role, 'provider': provider, 'call': call,
                      'input_fingerprint': fingerprint(message), 'state': 'dispatched',
                      'attempts': attempts, 'dispatched_at': time.time()}
    return records[op_id]


def received(project, op_id, reply, receipt=None):
    """The provider answered. The receipt hash is kept even when the reply later fails validation."""
    record = ledger(project)[op_id]
    body = json.dumps(reply, sort_keys=True) if not isinstance(reply, (bytes, str)) else reply
    record.update(state='received', receipt_sha256=fingerprint(body), receipt=receipt, received_at=time.time())
    return record


def failed(project, op_id, error, started=True):
    """The call failed. A failure before the provider process started is recorded as not dispatched."""
    record = ledger(project)[op_id]
    record.update(state='failed' if started else 'not_dispatched', error=str(error)[:500], failed_at=time.time())
    if not started:
        project.setdefault('events', []).append({'event': 'operation_not_dispatched', 'operation': op_id,
                                                 'at': record['failed_at'], 'counted': True})
    return record


def settled(project, op_id, valid, output_hashes=None):
    """Mark a received reply as committed or invalid after local validation. Both stay counted."""
    record = ledger(project).get(op_id)
    if not record or record.get('state') != 'received':
        return record
    record.update(state='committed' if valid else 'invalid', output_hashes=output_hashes or {}, settled_at=time.time())
    return record


def recover(project, kind, receipt_exists):
    """After a restart: dispatched calls with a receipt are received; without one they are uncertain."""
    uncertain = []
    for record in ledger(project).values():
        if record.get('kind') != kind or record.get('state') != 'dispatched':
            continue
        if receipt_exists(record):
            record.update(state='received', recovered_at=time.time())
        else:
            record.update(state='uncertain', detected_at=time.time())
            uncertain.append(record['id'])
    uncertain += [record['id'] for record in ledger(project).values()
                  if record.get('kind') == kind and record.get('state') == 'uncertain' and record['id'] not in uncertain]
    return uncertain


def guard(project, kind, receipt_exists):
    """Stop before dispatch when an earlier call of this kind has an uncertain outcome."""
    uncertain = recover(project, kind, receipt_exists)
    if uncertain:
        from reframe_states import stop
        stop('Uncertain dispatch: ' + ', '.join(sorted(uncertain)) + ' was dispatched and has no provider receipt. '
             'The call stays counted. No new call was made.', 'UNCERTAIN_DISPATCH',
             hint='Inspect the provider, then run reframe --workspace WORKSPACE reconcile-operation --id '
                  + sorted(uncertain)[0] + ' --resolution failed --by NAME --note REASON to continue with a new, counted call.')


def reconcile(project, op_id, resolution, by, note):
    """A person records the outcome of an uncertain call. The call stays counted."""
    record = ledger(project).get(op_id)
    require(record, 'Unknown operation ' + str(op_id))
    require(record.get('state') in {'uncertain', 'dispatched'}, 'Operation ' + op_id + ' is not uncertain')
    require(resolution in {'failed', 'received'}, 'Resolution must be failed or received')
    require(str(by).strip() and str(note).strip(), 'Reconciliation needs a named owner and a note')
    record.update(state='reconciled_' + resolution, reconciled_by=by, reconciled_note=note, reconciled_at=time.time())
    project.setdefault('events', []).append({'event': 'operation_reconciled', 'operation': op_id,
                                             'resolution': resolution, 'by': by, 'at': record['reconciled_at']})
    return record


def counts(project, kind=None):
    """Attempted, completed, invalid, failed, and uncertain calls, for the status view."""
    result = {'attempted': 0, 'completed': 0, 'invalid': 0, 'failed': 0, 'uncertain': 0, 'not_dispatched': 0}
    for record in ledger(project).values():
        if kind and record.get('kind') != kind:
            continue
        state = record.get('state')
        if state != 'not_dispatched':
            result['attempted'] += 1
        if state in {'committed', 'received', 'reconciled_received'}:
            result['completed'] += 1
        elif state == 'invalid':
            result['invalid'] += 1
        elif state in {'failed', 'reconciled_failed'}:
            result['failed'] += 1
        elif state in {'uncertain', 'dispatched'}:
            result['uncertain'] += 1
        elif state == 'not_dispatched':
            result['not_dispatched'] += 1
    return result
