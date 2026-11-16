"""A sanitized, deterministic specification at saved CardDemo scale.

The counts follow the saved CardDemo snapshot (452 SME questions, 112 checkpoint units,
a legacy wireframe request over 600 000 bytes). No text comes from the saved workspace:
every statement is generated from a fixed word list, so the fixture is portable and
carries no source, customer, or provider content.
"""
WORDS = ('account', 'card', 'balance', 'statement', 'transaction', 'customer', 'limit', 'interest', 'posting',
         'batch', 'screen', 'sign-on', 'cross-reference', 'date', 'amount', 'status', 'reject', 'accept', 'update',
         'report', 'window', 'file', 'record', 'key', 'cycle', 'fee', 'credit', 'debit', 'reversal', 'audit')

QUESTIONS = 452
DEFERRED = 54
RULES = 320
EVIDENCE = 120
SECTIONS = ('ui', 'data', 'batch', 'interfaces', 'security', 'reporting', 'operations', 'migration')


def text(seed, words):
    """Deterministic prose of a given word count. Different seeds give different text."""
    return ' '.join(WORDS[(seed * 7 + index * 13) % len(WORDS)] for index in range(words)).capitalize() + '.'


def specification():
    """A specification shaped like the saved CardDemo one, with generated text only."""
    rules = [{'id': f'R{index:04d}', 'statement': text(index, 190), 'evidence_status': 'SOURCE_VERIFIED',
              'source_path': f'app/cbl/PROG{index % 40:02d}.cbl', 'source_anchor': f'L{index * 3 + 1}'}
             for index in range(RULES)]
    questions = [{'id': f'Q{index:04d}', 'question': text(index + 1000, 30), 'impact': text(index + 2000, 12),
                  'owner': 'SME', 'blocks': 'Implementation of ' + WORDS[index % len(WORDS)]}
                 for index in range(QUESTIONS)]
    evidence = [{'id': f'E{index:04d}', 'statement': text(index + 3000, 60), 'evidence_status': 'ASSESSMENT_ONLY',
                 'assessment_path': f'assessment/batch-{index % 9}.json', 'assessment_anchor': f'#/{index}'}
                for index in range(EVIDENCE)]
    coverage = [{'id': rule['id'], 'kind': 'rule', 'disposition': 'mapped', 'gaps': [],
                 'source_path': rule['source_path'], 'source_anchor': rule['source_anchor']} for rule in rules]
    sections = {name: {'specification': text(index + 4000, 400)} for index, name in enumerate(SECTIONS)}
    return {'scope': 'Card management, sanitized fixture', 'excluded_scope': [], 'sections': sections,
            'rules': rules, 'questions': questions, 'assessment_evidence': evidence, 'coverage': coverage,
            'tests': [], 'work_items': []}


def decisions():
    """The first 54 questions carry saved deferrals; the rest are open."""
    return {f'Q{index:04d}': {'by': 'saved', 'answer': 'None', 'disposition': 'deferred', 'at': 1}
            for index in range(DEFERRED)}
