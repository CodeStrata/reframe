"""Checks on the handoff records inside any package ZIP (#107, #108, #109, #111, #113; SA-1)."""
import json
import re
import zipfile

import reframe_handoff as handoff

LANGUAGES = ('java', 'python', 'c#', '.net', 'typescript', 'javascript', 'spring', 'angular', 'react', 'node',
             'terraform', 'kubernetes')
# Files Reframe writes itself. Model-written prompts and a person's design plan may name a stack.
REFRAME_TEXT = handoff.NAMES | {'AGENTS.md', 'SKILL.md', 'README.md'}


def named_languages(text):
    """Language or toolkit words that appear as words in the text."""
    lowered = text.lower()
    return [word for word in LANGUAGES if re.search(r'(?<![a-z0-9])' + re.escape(word) + r'(?![a-z0-9])', lowered)]


def check(test, archive):
    """Assert every SA-1 handoff record and its open states in one archive."""
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        read = lambda name: json.loads(bundle.read(name))
        test.assertTrue(handoff.NAMES <= names, sorted(handoff.NAMES - names))
        sequence = read('modernization-sequence.json')
        test.assertEqual([step['id'] for step in sequence], [step for step, _ in handoff.STEPS])
        test.assertTrue(all(step['status'] == 'NOT_STARTED' for step in sequence))
        capabilities = read('capability-map.json')
        test.assertEqual(capabilities['acceptance'], 'PROPOSAL')
        test.assertTrue(capabilities['capabilities'])
        for item in capabilities['capabilities']:
            test.assertEqual(item['disposition'], 'unassigned')
            test.assertEqual(set(item['allowed_dispositions']) - {'unassigned'}, {'retain', 'expose', 'rewrite', 'retire'})
        plan = read('parallel-validation.json')
        cases = [case for rule in plan['rules'] for case in rule['cases']]
        test.assertTrue(cases)
        test.assertTrue(all(case['status'] == 'NOT RUN' and case['oracle'] == handoff.ORACLE for case in cases))
        test.assertNotIn('passed', json.dumps(plan).lower())
        governance = read('governance.json')
        test.assertEqual([gate['gate'] for gate in governance['retirement']], list(handoff.GATES))
        test.assertTrue(all(gate['status'] == 'PENDING' for gate in governance['retirement']))
        test.assertEqual(governance['retirement_status'], 'NOT_READY')
        test.assertTrue(governance['synthetic_data_only'])
        guide = read('extraction-reading.json')
        test.assertEqual(guide, handoff.extraction_reading(), 'the same reading guide on every route')
        for refused in ('Rewrite a member', 'Remove a member from the pinned source', 'Submit a replacement archive'):
            test.assertIn(refused, guide['refused_actions'])
        test.assertIn('extraction-reading.json', bundle.read('skill-extraction.md').decode())
        test.assertTrue({'skill-discovery.md', 'skill-rules.md', 'skill-data.md', 'skill-api.md', 'skill-screens.md',
                         'skill-batch.md', 'skill-tests.md', 'skill-risk.md', 'skill-extraction.md'} <= names)
        for name in sorted(REFRAME_TEXT & names):
            test.assertEqual(named_languages(bundle.read(name).decode()), [], name + ' names a language or toolkit')
        legacy = read('legacy-requirements.json')
        test.assertIn('files', legacy)
        return names
