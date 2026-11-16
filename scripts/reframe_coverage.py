"""Requirement coverage, test-template readiness, and SME question views (FR-06).

Coverage comes only from structured id lists. Prose never creates a mapping.
A generated test stays a placeholder until it states preconditions, inputs,
expected results, and an oracle or a named oracle gap. Question groups are
suggestions built from identical structured fields; every original question
and its id stays as it was.
"""

TEST_FIELDS = (('preconditions',), ('inputs', 'steps'), ('expected', 'expected_result'), ('oracle', 'oracle_gap'))


def _references(spec):
    """Which sections, work items, and tests list each id in a structured field."""
    refs = {}

    def add(ident, kind, owner):
        if isinstance(ident, str) and ident:
            refs.setdefault(ident, {'sections': [], 'work_items': [], 'tests': []})[kind].append(owner)

    for name, section in (spec.get('sections') or {}).items():
        if isinstance(section, dict):
            for ident in (section.get('rule_ids') or []) + (section.get('requirement_ids') or []):
                add(ident, 'sections', name)
    for item in spec.get('work_items') or []:
        if isinstance(item, dict):
            for ident in (item.get('rule_ids') or []) + (item.get('requirement_ids') or []):
                add(ident, 'work_items', item.get('id'))
    for case in spec.get('tests') or []:
        if isinstance(case, dict):
            for ident in [case.get('rule_id')] + (case.get('requirement_ids') or []):
                add(ident, 'tests', case.get('id'))
    return refs


def requirement_coverage(spec, requirement_ids):
    """One row per requirement: mapped, gap, or excluded with a recorded reason."""
    refs = _references(spec)
    excluded = spec.get('excluded_requirements') if isinstance(spec.get('excluded_requirements'), dict) else {}
    rows = []
    for ident in requirement_ids:
        if excluded.get(ident):
            rows.append({'id': ident, 'kind': 'requirement', 'disposition': 'excluded', 'reason': excluded[ident], 'gaps': []})
            continue
        found = refs.get(ident) or {'sections': [], 'work_items': [], 'tests': []}
        gaps = [name for name in ('sections', 'work_items', 'tests') if not found[name]]
        rows.append({'id': ident, 'kind': 'requirement', 'disposition': 'mapped' if not gaps else 'gap',
                     'gaps': gaps, **found})
    return rows


def test_templates(spec):
    """Each test is CONCRETE only with preconditions, inputs, expected results, and an oracle or oracle gap."""
    rows = []
    for case in spec.get('tests') or []:
        if not isinstance(case, dict):
            continue
        missing = [names[0] for names in TEST_FIELDS
                   if not any(case.get(name) not in (None, '', [], {}) for name in names)]
        rows.append({'id': case.get('id'), 'state': 'CONCRETE' if not missing else 'PLACEHOLDER', 'missing': missing,
                     'execution': case.get('status') or 'NOT RUN'})
    return rows


def annotate(spec, requirement_ids):
    """Add requirement coverage and test-template states. Rule coverage stays where synthesis put it."""
    spec['requirement_coverage'] = requirement_coverage(spec, requirement_ids)
    spec['test_templates'] = test_templates(spec)
    return spec


def _state(question, decisions):
    decision = decisions.get(question.get('id'))
    if not isinstance(decision, dict):
        return 'open'
    return decision.get('disposition') or 'open'


def question_rows(spec, decisions):
    """Every SME question with its owner, impact, blocked work, structured references, and decision state."""
    rows = []
    for question in spec.get('questions') or []:
        if not isinstance(question, dict) or not question.get('id'):
            continue
        rows.append({'id': question['id'], 'owner': question.get('owner'), 'impact': question.get('impact'),
                     'blocks': question.get('blocks'), 'severity': question.get('severity') or 'not recorded',
                     'rule_ids': sorted(question.get('rule_ids') or []),
                     'function_ids': sorted(question.get('function_ids') or []),
                     'state': _state(question, decisions), 'question': question.get('question')})
    return rows


def filter_questions(rows, owner=None, state=None, rule=None, function=None, blocks=None, severity=None):
    """Filter on recorded fields only. A field a question does not record never matches a filter on it."""
    def keep(row):
        return ((not owner or row['owner'] == owner) and (not state or row['state'] == state)
                and (not rule or rule in row['rule_ids']) and (not function or function in row['function_ids'])
                and (not blocks or (row['blocks'] or '').casefold() == blocks.casefold())
                and (not severity or row['severity'] == severity))
    return [row for row in rows if keep(row)]


def suggested_groups(rows):
    """Questions that share owner, blocked work, and structured rule ids. A suggestion; nothing is merged."""
    groups = {}
    for row in rows:
        key = (row['owner'], (row['blocks'] or '').strip().casefold(), tuple(row['rule_ids']))
        groups.setdefault(key, []).append(row['id'])
    return [{'owner': key[0], 'blocks': key[1], 'rule_ids': list(key[2]), 'question_ids': ids,
             'basis': 'same owner, blocked work, and rule ids; questions stay separate'}
            for key, ids in groups.items() if len(ids) > 1]


def summary(rows):
    """Counts by state and owner, for one status line instead of one box per question."""
    by_state, by_owner = {}, {}
    for row in rows:
        by_state[row['state']] = by_state.get(row['state'], 0) + 1
        by_owner[row['owner'] or 'unassigned'] = by_owner.get(row['owner'] or 'unassigned', 0) + 1
    return {'total': len(rows), 'by_state': by_state, 'by_owner': by_owner}
