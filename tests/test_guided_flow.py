"""Guided flow routing: no AWS or model calls."""
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
os.environ.setdefault('REFRAME_CONFIG_HOME', tempfile.mkdtemp(prefix='reframe-guided-config-'))
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).parents[1]/'scripts'))
from reframe_flow import run
from reframe_flow import offer_context as real_offer_context  # setUp stubs the module attribute
from reframe_terminal import Terminal
from rich.console import Console

class GuidedFlowTests(unittest.TestCase):
    def setUp(self):
        """Routing tests stub the review-gate helpers; tests/test_flow_gates.py covers the gates themselves."""
        for name in ('baseline_inputs', 'offer_context', 'ensure_design_plan'):
            stub = patch('reframe_flow.' + name, return_value=True)
            stub.start()
            self.addCleanup(stub.stop)

    def test_conflict_prompt_uses_keep_human_statement(self):
        from reframe_flow import finish_guided_design
        import reframe_optional as optional
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            (folder / 'project.json').write_text('{"stage":"PACKAGED","settings":{}}')
            note = folder / 'human.md'
            note.write_text('Contradicts: R1\nThe cutoff is 9.\n')
            imported = optional.import_context(folder, note, 'Ari', 'architect', 'current-state', ['s1'])
            optional.decide_context(folder, imported['id'], 'accepted', 'Ari', 'Recorded')
            ui = self.ui({'stage': 'PACKAGED', 'settings': {}, 'approvals': {}}, [
                'functional-parity', 'v1', 'unspecified', str(note), 'Ari', 'architect', 'current-state', 's1', 'rejected',
                'keep-human-statement', 'Ari', 'Use the human statement',
            ], gates=False)
            ui.yes.return_value = True
            with patch('reframe_setup.workspace', return_value=folder):
                finish_guided_design(ui, ui.project())
        prompts = [call.args[0] for call in ui.ask.call_args_list]
        self.assertTrue(any('keep-human-statement' in prompt for prompt in prompts))
        self.assertFalse(any('keep-context' in prompt for prompt in prompts))
        resolved = [call.args[0] for call in ui.invoke.call_args_list if call.args[0][0] == 'context' and 'resolve' in call.args[0]]
        self.assertEqual(resolved[0][resolved[0].index('--resolution') + 1], 'keep-human-statement')
    GATE_ANSWERS = (
        ('Your name for these review records', 'Reviewer'),
        ('Who ', 'Reviewer'),
        ('Markdown context for the ', 'none'),
        ('Business requirements (', 'none'),
        ('Design mode (functional-parity/reimagine)', 'functional-parity'),
        ('Design version', 'v1'),
        ('Target language or stack', 'unspecified'),
        ('Architecture constraints', 'none'),
        ('Design decision (', 'pause'),
        ('Package decision (', 'pause'),
        ('Request a specification change now', 'pause'),
    )

    GATE_COMMANDS = {('requirements', 'status'), ('requirements', 'none'), ('context', 'none'), ('design-plan',)}

    def routed(self, ui):
        """Invoked commands, without the review-gate records that every journey now writes."""
        calls = [call.args[0] for call in ui.invoke.call_args_list]
        return [c for c in calls if tuple(c[:2]) not in self.GATE_COMMANDS and tuple(c[:1]) not in self.GATE_COMMANDS]

    def gates(self, ui):
        """The review-gate commands this run wrote."""
        calls = [call.args[0] for call in ui.invoke.call_args_list]
        return [c for c in calls if tuple(c[:2]) in self.GATE_COMMANDS or tuple(c[:1]) in self.GATE_COMMANDS]

    def ui(self, project, answers, gates=True):
        """Scripted answers for routing; with gates, the review-gate questions get their documented defaults."""
        ui = Mock()
        ui.project.return_value = project
        ui.reviewer_name = None
        ui.last_report = {}
        scripted = list(answers)

        def ask(prompt, *args, **kwargs):
            for prefix, answer in self.GATE_ANSWERS if gates else ():
                if prompt.startswith(prefix):
                    return answer
            return scripted.pop(0)

        ui.ask.side_effect = ask
        ui.invoke.return_value = 0
        return ui

    def test_skip_never_runs_verification_or_approved_package(self):
        ui = self.ui({'stage':'BLOCKED','approvals':{'assessment':True}},
                     ['continue','draft','guided-draft','Owner','Demo','claude'])
        ui.yes.return_value = True
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        commands = [c[0] for c in self.routed(ui)]
        self.assertEqual(commands, ['preview'])
        self.assertIn('--skip-validation', self.routed(ui)[0])
        self.assertNotIn('validate', commands)
        self.assertNotIn('approve', commands)
        self.assertNotIn('package', commands)
        prompts = [call.args[0] for call in ui.ask.call_args_list]
        self.assertTrue(any(prompt.startswith('Design decision') for prompt in prompts))
        self.assertNotIn('package', commands)

    def test_review_declined_never_approves(self):
        ui = self.ui({'stage':'AWAITING_ASSESSMENT_APPROVAL'}, ['continue'])
        ui.yes.return_value = False
        run(ui)
        self.assertEqual(self.routed(ui), [['assessment-report']])

    def test_rework_limit_resumes_without_a_new_assessment(self):
        project = {'stage': 'REWORK_LIMIT', 'approvals': {'assessment': True},
                   'pipeline': {'calls': 4, 'status': 'REWORK_LIMIT'},
                   'checkpoints': {'status': 'PLANNED', 'units': {}}}
        ui = self.ui(project, ['continue'])
        ui.last_report = {'unit': 'U0001', 'next_step': 'reframe feedback --unit U0001 --authorize-correction --by NAME --note REASON'}
        run(ui)
        commands = self.routed(ui)
        self.assertEqual(commands, [['resume']])
        said = ' '.join(str(call.args[0]) for call in ui.say.call_args_list)
        self.assertIn('U0001', said)
        self.assertIn('No new assessment job is created.', said)
        self.assertNotIn('assess', str(commands))

    def test_invalid_correction_resume_stays_on_the_saved_review(self):
        project = {'stage': 'RUNNING_EXECUTOR', 'approvals': {'assessment': True},
                   'pipeline': {'calls': 301, 'status': 'RUNNING', 'role': 'executor', 'limit_corrections': 1,
                                'correction_error': {'call': 301, 'reason': 'Correction target must be the string section or work_item; received dict'}},
                   'checkpoints': {'status': 'READY_FOR_SYNTHESIS', 'units': {'U0001': {'status': 'PASS'}}}}
        ui = self.ui(project, ['continue'])
        calls = []

        def invoke(args):
            calls.append(args)
            if len(calls) == 1:
                return 2
            ui.project.return_value = {'stage': 'AWAITING_VALIDATION_APPROVAL', 'approvals': {'assessment': True},
                                      'pipeline': {}, 'settings': {}}
            return 0

        ui.invoke.side_effect = invoke
        ui.yes.return_value = False
        ui.last_report = {'status': 'CORRECTION_INVALID',
                          'reason': project['pipeline']['correction_error']['reason'],
                          'next_step': 'reframe resume. The saved correction was rejected before any edit was applied.'}
        run(ui)
        self.assertEqual(calls, [['resume'], ['resume']])
        said = ' '.join(str(call.args[0]) for call in ui.say.call_args_list)
        self.assertIn('received dict', said)
        self.assertIn('Continuing the saved review', said)
        self.assertNotIn('approve', str(calls))

    def test_running_assessment_resumes_without_new_job(self):
        ui = self.ui({'stage':'ASSESSING','active_assessment':'run-1'}, ['continue'])
        run(ui)
        self.assertEqual(self.routed(ui), [['resume','--wait']])

    def test_failed_setup_stops(self):
        ui = self.ui(None, ['https://github.com/example/new.git'])
        ui.invoke.return_value = 2
        run(ui)
        self.assertEqual(self.routed(ui), [['init', '--guided', '--source', 'https://github.com/example/new.git']])

    def test_verify_failure_never_falls_back_to_draft(self):
        ui = self.ui({'stage':'ASSESSMENT_APPROVED','approvals':{'assessment':True}}, ['continue','verify'])
        ui.yes.return_value = True
        ui.invoke.return_value = 2
        run(ui)
        self.assertEqual(self.routed(ui), [['validate']])

    def test_validation_gate_does_not_restart_verification(self):
        ui = self.ui({'stage':'AWAITING_VALIDATION_APPROVAL','approvals':{'assessment':True}}, ['continue'])
        ui.yes.return_value = False
        run(ui)
        self.assertEqual(self.routed(ui), [])

    def test_demo_flow_cannot_invoke_backend(self):
        ui = Terminal(console=Console(file=io.StringIO()), demo=True)
        with patch.object(ui, 'invoke', side_effect=AssertionError('Live call')):
            ui.dispatch('/flow')
            ui.dispatch('1')

    def test_saved_draft_reuses_original_decision_and_provider(self):
        import json
        ui = self.ui({'stage':'ASSESSMENT_APPROVED','approvals':{'assessment':True}},
                     ['continue','draft','guided-draft'])
        ui.yes.return_value = True
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            saved = Path(root)/'previews'/'guided-draft'
            saved.mkdir(parents=True)
            (saved/'preview-state.json').write_text(json.dumps({'owner':'Owner','reason':'Accepted risk','provider':'claude'}))
            run(ui)
        args = self.routed(ui)[0]
        self.assertIn('Accepted risk', args)
        self.assertIn('claude', args)
        prompts = [call.args[0] for call in ui.ask.call_args_list]
        self.assertFalse(any('Accountable owner' in prompt or 'Reason for trusting' in prompt for prompt in prompts),
                         'the saved owner and reason are reused, not asked again')
        self.assertEqual(ui.ask.call_count, 4)

    def test_skip_confirmation_declined_has_no_provider_call(self):
        ui = self.ui({'stage':'ASSESSMENT_APPROVED','approvals':{'assessment':True}},
                     ['continue','draft','guided-draft','Owner','Demo','claude'])
        ui.yes.return_value = False
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        self.assertEqual(self.routed(ui), [])

    def test_skip_word_generates_the_draft_package(self):
        ui = self.ui({'stage':'ASSESSMENT_APPROVED','approvals':{'assessment':True},
                      'providers':{'wireframes':'claude'}},
                     ['continue','skip','guided-draft','Owner','Accepted risk','claude'])
        ui.yes.return_value = True
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        args = self.routed(ui)[0]
        self.assertEqual(args[0], 'preview')
        self.assertIn('--skip-validation', args)
        self.assertEqual(self.routed(ui), [args], 'the skip draft stops at design review; nothing is approved or packaged')

    def test_short_review_budget_states_the_count_before_raising_it(self):
        first = {'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True}}
        blocked = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'pipeline':{
            'calls':0, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':12, 'remaining_calls':4}}
        ready = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}}
        ui = self.ui(first, ['continue', 'review', 'Owner', 'Cover the paired programs'])
        ui.project.side_effect = [first, first, blocked, ready]
        ui.invoke.side_effect = [2, 0, 0]
        ui.yes.side_effect = [True, True, False]
        lines = self.said(ui)
        run(ui)
        self.assertIn('at least 12 more model calls', '\n'.join(lines))
        self.assertEqual(ui.invoke.call_args_list[1].args[0],
                         ['model-budget', '--max-calls', '12', '--by', 'Owner', '--note', 'Cover the paired programs'])
        self.assertEqual(ui.invoke.call_args_list[2].args[0], ['validate'])

    def test_spent_calls_ask_to_raise_the_cap_above_what_was_used(self):
        first = {'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True}}
        blocked = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'pipeline':{
            'calls':3, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':142, 'remaining_calls':139}}
        ready = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}}
        ui = self.ui(first, ['continue', 'review', 'Satish', 'Need more to run'])
        ui.project.side_effect = [first, first, blocked, ready]
        ui.invoke.side_effect = [2, 0, 0]
        ui.yes.side_effect = [True, True, False]
        lines = self.said(ui)
        run(ui)
        text = '\n'.join(lines)
        self.assertIn('at least 142 more model calls', text)
        self.assertIn('3 model calls were already used', text)
        self.assertEqual(ui.yes.call_args_list[1].args[0], 'Raise the model-call cap to 145 and start the review?')
        self.assertEqual(ui.invoke.call_args_list[1].args[0],
                         ['model-budget', '--max-calls', '145', '--by', 'Satish', '--note', 'Need more to run'])
        self.assertEqual(ui.invoke.call_args_list[2].args[0], ['validate'])

    def test_exhausted_budget_restates_the_remaining_plan_before_asking(self):
        first = {'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True}}
        exhausted = {'stage':'BLOCKED', 'approvals':{'assessment':True}, 'pipeline':{
            'calls':148, 'reason':'Total model call budget exhausted'}}
        blocked = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'pipeline':{
            'calls':148, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':40, 'remaining_calls':0}}
        ready = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}}
        ui = self.ui(first, ['continue', 'review', 'Satish', 'Finish the remaining programs'])
        ui.project.side_effect = [first, first, exhausted, blocked, ready]
        ui.invoke.side_effect = [2, 2, 0, 0]
        ui.yes.side_effect = [True, True, False]
        lines = self.said(ui)
        run(ui)
        self.assertIn('at least 40 more model calls', '\n'.join(lines))
        self.assertEqual(ui.invoke.call_args_list[1].args[0], ['validate'])
        self.assertEqual(ui.yes.call_args_list[1].args[0], 'Raise the model-call cap to 188 and start the review?')
        self.assertEqual(ui.invoke.call_args_list[2].args[0],
                         ['model-budget', '--max-calls', '188', '--by', 'Satish', '--note', 'Finish the remaining programs'])

    def test_a_large_estate_can_raise_the_allowance_past_256(self):
        first = {'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True}, 'settings':{'max_model_calls':256}}
        blocked = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'settings':{'max_model_calls':256}, 'pipeline':{
            'calls':256, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':7, 'remaining_calls':0}}
        ready = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}}
        ui = self.ui(first, ['continue', 'review', 'Satish', 'Finish the remaining programs'])
        ui.project.side_effect = [first, first, blocked, ready]
        ui.invoke.side_effect = [2, 0, 0]
        ui.yes.side_effect = [True, True, False]
        run(ui)
        self.assertEqual(ui.yes.call_args_list[1].args[0], 'Raise the model-call cap to 263 and start the review?')
        self.assertEqual(ui.invoke.call_args_list[1].args[0],
                         ['model-budget', '--max-calls', '263', '--by', 'Satish', '--note', 'Finish the remaining programs'])

    def test_a_raise_that_is_spent_asks_for_the_next_cap(self):
        first = {'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True}}
        blocked = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'pipeline':{
            'calls':200, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':2, 'remaining_calls':0}}
        exhausted = {'stage':'BLOCKED', 'approvals':{'assessment':True}, 'settings':{'max_model_calls':202}, 'pipeline':{
            'calls':202, 'reason':'Total model call budget exhausted'}}
        blocked_again = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'settings':{'max_model_calls':202}, 'pipeline':{
            'calls':202, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':2, 'remaining_calls':0}}
        ready = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}}
        ui = self.ui(first, ['continue', 'review', 'Satish', 'Finish synthesis', 'Satish', 'Finish synthesis'])
        ui.project.side_effect = [first, first, blocked, exhausted, blocked_again, ready]
        ui.invoke.side_effect = [2, 0, 2, 2, 0, 0]
        ui.yes.side_effect = [True, True, True, False]
        lines = self.said(ui)
        run(ui)
        self.assertEqual(ui.yes.call_args_list[2].args[0], 'Raise the model-call cap to 204 and start the review?')
        self.assertIn('Checking how many calls', '\n'.join(lines))

    def test_open_questions_are_deferred_before_validation_approval(self):
        waiting = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}, 'decisions':{}}
        approved = {'stage':'VALIDATION_APPROVED', 'approvals':{'assessment':True, 'validation':True}}
        ui = self.ui(waiting, ['continue', 'Satish', 'Deferred for package review'])
        ui.yes.side_effect = [True, True]

        def invoke(args):
            if args[0] == 'approve':
                ui.project.return_value = approved
            return 0 if args[0] != 'review-site' else 2

        ui.invoke.side_effect = invoke
        with patch('reframe_flow.open_question_ids', return_value=['Q1', 'Q2']):
            run(ui)
        calls = [c.args[0] for c in ui.invoke.call_args_list]
        self.assertEqual(calls[0], ['decide', '--open', '--by', 'Satish', '--answer', 'Deferred for package review',
                                    '--disposition', 'deferred', '--confirm'])
        self.assertEqual(calls[1], ['approve', 'validation'])
        self.assertEqual(len([call for call in calls if call[0] == 'decide']), 1)

    def test_declining_deferral_records_no_approval(self):
        waiting = {'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True}, 'decisions':{}}
        ui = self.ui(waiting, ['continue'])
        ui.yes.return_value = False
        with patch('reframe_flow.open_question_ids', return_value=['Q1']):
            run(ui)
        self.assertEqual(self.routed(ui), [])

    def test_review_word_runs_validation(self):
        ui = self.ui({'stage':'ASSESSMENT_APPROVED','approvals':{'assessment':True}}, ['continue','review'])
        ui.yes.return_value = True
        ui.invoke.return_value = 2
        run(ui)
        self.assertEqual(self.routed(ui), [['validate']])

    def test_framework_update_is_recorded_before_approval(self):
        stale = {'stage':'AWAITING_ASSESSMENT_APPROVAL','framework_commit':'old','approvals':{}}
        ui = self.ui(stale, ['continue', 'Record the controller update'])
        ui.project.side_effect = [stale, stale]
        ui.yes.return_value = False
        with patch('reframe.git', return_value='new'):
            run(ui)
        self.assertEqual(self.routed(ui)[0],
                         ['upgrade-framework', '--note', 'Record the controller update'])
        self.assertEqual(ui.invoke.call_args_list[1].args[0], ['assessment-report'])

    def said(self, ui):
        lines = []
        ui.say.side_effect = lines.append
        return lines

    def test_assessment_review_names_the_html_and_sealed_findings(self):
        with tempfile.TemporaryDirectory() as root:
            run_dir = Path(root) / 'runs' / 'run-1'
            ui = self.ui({'stage':'AWAITING_ASSESSMENT_APPROVAL', 'active_assessment':'run-1',
                          'assessments':{'run-1':{'directory':str(run_dir)}}}, ['continue'])
            ui.yes.return_value = False
            lines = self.said(ui)
            run(ui)
        text = '\n'.join(lines)
        self.assertIn('Assessment review page — HTML — ' + str(run_dir / 'assessment-review.html'), text)
        self.assertIn('Sealed findings — ZIP, CSV, JSON, and PDF — ' + str(run_dir / 'assessment'), text)
        self.assertIn('Report index — HTML — ' + str(Path(root) / 'reports' / 'index.html'), text)

    def test_validation_review_names_the_html_and_json(self):
        ui = self.ui({'stage':'AWAITING_VALIDATION_APPROVAL', 'approvals':{'assessment':True},
                      'specification':{'path':'preparation/candidate-1.json', 'review_path':'preparation/review-1.json'}},
                     ['continue'])
        ui.yes.return_value = False
        lines = self.said(ui)
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        text = '\n'.join(lines)
        self.assertIn('SME and architect review — HTML — ' + str(Path(root) / 'preparation' / 'review.html'), text)
        self.assertIn('Executor candidate — JSON — ' + str(Path(root) / 'preparation' / 'candidate-1.json'), text)
        self.assertIn('Independent reviewer report — JSON — ' + str(Path(root) / 'preparation' / 'review-1.json'), text)
        self.assertEqual(self.routed(ui), [])

    def test_a_missing_context_path_is_asked_again_before_other_questions(self):
        from reframe_flow import ask_existing_file
        with tempfile.TemporaryDirectory() as root:
            real = Path(root) / 'note.md'
            real.write_text('note')
            ui = self.ui({}, [str(Path(root) / 'missing.md'), str(real)], gates=False)
            lines = self.said(ui)
            self.assertEqual(ask_existing_file(ui, 'Markdown context for the design review, or none', allow_none=True), str(real))
            self.assertIn('No file was found at that path', '\n'.join(lines))
            self.assertEqual(ui.ask.call_count, 2, 'no category or role question came before the path was valid')
            ui = self.ui({}, ['a', 'b', 'c'], gates=False)
            self.assertIsNone(ask_existing_file(ui, 'Path to requirements.md'))

    def test_each_approval_asks_who_approves_and_a_yes_is_not_a_name(self):
        from reframe_flow import approver, reviewer
        from pilot import Blocked
        ui = self.ui({}, ['y', 'no', 'y'], gates=False)
        with self.assertRaisesRegex(Blocked, 'not "y"'):
            reviewer(ui)
        ui = self.ui({}, ['y', 'Dana'], gates=False)
        self.assertEqual(reviewer(ui), 'Dana', 'a refused session name is asked again, not sent back to the menu')
        ui = self.ui({}, ['Dana', 'Lee'], gates=False)
        self.assertEqual(approver(ui, 'approves this design'), 'Lee')
        self.assertEqual(ui.ask.call_args_list[-1].args, ('Who approves this design? Their name is recorded on it', 'Dana'))

    def test_a_completed_design_version_explains_how_to_start_the_next(self):
        from reframe_flow import design_review
        ui = self.ui({'stage': 'AWAITING_SPECIFICATIONS_APPROVAL'}, [])
        ui.reviewer_name = 'Reviewer'

        def invoke(command):
            if command[0] == 'design-export':
                ui.last_report = {'status': 'BLOCKED', 'reason': 'Completed version v1 is immutable. The next revision is v2.'}
                return 2
            return 0

        ui.invoke.side_effect = invoke
        lines = self.said(ui)
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            outcome = design_review(ui, {'design_plan': {'mode': 'reimagine', 'version': 'v1', 'target': {}}}, skip_route=False)
        self.assertEqual(outcome, 'stop', 'the gate pauses by default; nothing is approved')
        self.assertIn('through design-change, which starts the next version', ' '.join(' '.join(lines).split()))

    def test_deferring_a_conflict_records_it_and_keeps_it_open(self):
        from reframe_flow import offer_open_conflicts
        conflict = {'id': 'conflict-ctx-1', 'contradicts': 'R1', 'status': 'open'}
        ui = self.ui({'stage': 'AWAITING_VALIDATION_APPROVAL'}, ['Dana', 'Waiting for the business owner'], gates=False)
        ui.yes.side_effect = [False, True]
        lines = self.said(ui)
        with patch('reframe_optional.open_conflicts', return_value=[conflict]):
            self.assertTrue(offer_open_conflicts(ui, Path('/nowhere')))
        self.assertEqual(ui.invoke.call_args.args[0], ['context', 'resolve', '--id', 'conflict-ctx-1', '--resolution',
                                                       'needs-more-evidence', '--by', 'Dana', '--note', 'Waiting for the business owner'])
        self.assertIn('keeps blocking the approvals it affects', '\n'.join(lines))

    def test_a_failed_wireframe_call_is_offered_again_and_an_authorized_attempt_runs(self):
        project = {'stage': 'BLOCKED', 'approvals': {'assessment': True, 'validation': True}}
        failed = [{'index': 0, 'status': 'failed'}]
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)), \
                patch('reframe.failed_wireframe_stages', side_effect=lambda *_a: failed):
            ui = self.ui(project, ['continue'], gates=False)
            ui.yes.return_value = False
            lines = self.said(ui)
            run(ui)
            self.assertIn('/flow offers the new attempt again', '\n'.join(lines))
            self.assertEqual([call.args[0] for call in ui.invoke.call_args_list], [], 'declining changes nothing')
            ui = self.ui(project, ['continue', 'y', 'Dana', 'The provider outage is over'], gates=False)
            ui.reviewer_name = 'Ari'
            ui.yes.return_value = True
            lines = self.said(ui)

            def invoke(command):
                if command[0] == 'review-site':
                    failed.clear()
                return 0

            ui.invoke.side_effect = invoke
            run(ui)
        invoked = [call.args[0] for call in ui.invoke.call_args_list]
        self.assertEqual(invoked[:2], [['retry-wireframes', '--by', 'Dana', '--note', 'The provider outage is over'],
                                       ['review-site']])
        self.assertIn('Enter a person\'s name, not "y"', '\n'.join(lines))

    def test_a_duplicate_or_credential_context_file_is_refused_before_other_questions(self):
        import reframe_optional as optional
        offer_context = real_offer_context
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            (folder / 'project.json').write_text('{"stage":"AWAITING_VALIDATION_APPROVAL","settings":{}}')
            note = folder / 'note.md'
            note.write_text('The cutoff is 9.\n')
            optional.import_context(folder, note, 'Ari', 'architect', 'clarification', [])
            secret = folder / 'secret.md'
            secret.write_text('token AKIAIOSFODNN7EXAMPLE\n')
            ui = self.ui({}, [str(note), str(secret), 'none'], gates=False)
            ui.reviewer_name = 'Ari'
            lines = self.said(ui)
            with patch('reframe_setup.workspace', return_value=folder):
                self.assertTrue(offer_context(ui, 'specification'))
        prompts = [call.args[0] for call in ui.ask.call_args_list]
        self.assertFalse(any(prompt.startswith('Context category') for prompt in prompts), 'refused before the category')
        text = '\n'.join(lines)
        self.assertIn('already imported', text)
        self.assertIn('looks like a cloud access key', text)
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', text)
        self.assertEqual(ui.invoke.call_args.args[0][:2], ['context', 'none'])

    def test_a_package_refused_for_accepted_context_offers_to_reject_it(self):
        from reframe_flow import offer_withdraw_flagged_context, masked
        import reframe_optional as optional
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            (folder / 'project.json').write_text('{"stage":"DESIGN_APPROVED","settings":{}}')
            note = folder / 'note.md'
            note.write_text('The cutoff is 9.\n')
            record = optional.import_context(folder, note, 'Ari', 'architect', 'clarification', [])
            optional.decide_context(folder, record['id'], 'accepted', 'Ari', 'Recorded')
            # A note stored before import-time refusal existed.
            (optional.context_dir(folder) / 'extracted' / (record['id'] + '.txt')).write_text('token AKIAIOSFODNN7EXAMPLE\n')
            ui = self.ui({}, ['Dana', 'Contains a credential-shaped value'], gates=False)
            ui.reviewer_name = 'Ari'
            ui.yes.return_value = True
            ui.last_report = {'reason': 'Refusing package; human-context.json matches cloud access key'}
            lines = self.said(ui)
            with patch('reframe_setup.workspace', return_value=folder):
                offer_withdraw_flagged_context(ui)
        self.assertEqual(ui.invoke.call_args.args[0], ['context', 'decide', '--id', record['id'], '--disposition', 'rejected',
                                                       '--by', 'Dana', '--note', 'Contains a credential-shaped value'])
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', '\n'.join(lines))
        self.assertEqual(masked('key AKIAIOSFODNN7EXAMPLE here'), 'key [hidden value] here')

    def test_the_skip_route_next_step_never_names_validate(self):
        from reframe_setup import next_step
        base = {'stage': 'ASSESSMENT_APPROVED', 'verification_skip': {'owner': 'Ari'}, 'settings': {}}
        with patch('reframe.prompts_differ', return_value=False):
            for extra in ({}, {'skip_bundle': 'previews/d'}, {'skip_bundle': 'previews/d', 'approvals': {'design': {}}}):
                self.assertNotIn('validate', next_step({**base, **extra}))
            self.assertIn('approve design', next_step({**base, 'skip_bundle': 'previews/d'}))

    def test_menu_8_offers_the_same_recovery_when_context_blocks_the_package(self):
        ui = Terminal(console=Console(file=io.StringIO()), demo=False)
        with patch.object(ui, 'invoke', return_value=2), \
                patch('reframe_flow.offer_withdraw_flagged_context') as offered:
            ui.dispatch('8')
        offered.assert_called_once_with(ui)

    def test_an_unknown_delta_id_is_refused_before_the_approver_is_asked(self):
        from reframe_flow import ask_proposal_id
        ui = self.ui({}, ['P9', 'P1'], gates=False)
        lines = self.said(ui)
        self.assertEqual(ask_proposal_id(ui, ['P1', 'P2'], 'Approve one future-state delta by id, or none', 'none'), 'P1')
        self.assertIn('No proposal P9 is recorded for this version. Proposals: P1, P2.', lines)
        ui = self.ui({}, ['P7', 'P8', 'P9'], gates=False)
        self.assertIsNone(ask_proposal_id(ui, ['P1'], 'Proposal id to approve', None))
        self.assertEqual(ui.ask.call_count, 3, 'no approver or rationale is asked for an unknown id')

    def test_before_a_route_is_chosen_the_next_step_presumes_neither(self):
        from reframe_setup import next_step
        with patch('reframe.prompts_differ', return_value=False):
            text = next_step({'stage': 'ASSESSMENT_APPROVED', 'design_plan': {'mode': 'reimagine'}, 'settings': {}})
        self.assertTrue(text.startswith('Choose a route with /flow'), text)
        self.assertIn('preview --skip-validation', text)

    def test_specifications_review_names_the_wireframes_and_json(self):
        ui = self.ui({'stage':'AWAITING_SPECIFICATIONS_APPROVAL', 'approvals':{'assessment':True, 'validation':True},
                      'site':{'directory':'previews/business-1'}}, ['continue'])
        lines = self.said(ui)
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        text = '\n'.join(lines)
        site = Path(root) / 'previews' / 'business-1'
        for label, kind, name in (('Business review wireframes', 'HTML', 'index.html'), ('Screen content', 'JSON', 'screens.json'),
                                  ('API contracts', 'JSON', 'api-contracts.json'), ('OpenAPI document', 'JSON', 'openapi.json')):
            self.assertIn(label + ' — ' + kind + ' — ' + str(site / name), text)
        self.assertIn('Paused for human review. No approval was recorded.', text)
        self.assertFalse([call for call in self.routed(ui) if call[0] == 'approve'])

    def test_declining_both_cap_choices_makes_no_model_call(self):
        first = {'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True}}
        blocked = {'stage':'PREPARATION_PLANNED', 'approvals':{'assessment':True}, 'pipeline':{
            'calls':0, 'reason':'Insufficient call budget for remaining checkpoint plan',
            'minimum_additional_calls':12, 'remaining_calls':4}}
        ui = self.ui(first, ['continue', 'review'])
        ui.project.side_effect = [first, first, blocked, blocked]
        ui.invoke.side_effect = [2]
        ui.yes.side_effect = [True, False, False]
        lines = self.said(ui)
        run(ui)
        text = '\n'.join(lines)
        self.assertIn('at least 12 more model calls', text)
        self.assertIn('No model call was made', text)
        invoked = [call.args[0] for call in ui.invoke.call_args_list]
        self.assertEqual(len([call for call in invoked if call[0] == 'validate']), 1, 'only the first planning attempt')
        self.assertFalse([call for call in invoked if call[0] == 'model-budget'])

    def test_skip_names_the_html_wireframes_and_zip(self):
        ui = self.ui({'stage':'ASSESSMENT_APPROVED', 'approvals':{'assessment':True},
                      'providers':{'wireframes':'claude'}},
                     ['continue', 'skip', 'guided-draft', 'Owner', 'Accepted risk', 'claude',
                      'functional-parity', 'v1', 'unspecified', 'none'])
        ui.yes.return_value = True
        lines = self.said(ui)
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        text = '\n'.join(lines)
        self.assertIn('Wireframes — HTML — ' + str(Path(root) / 'previews' / 'guided-draft' / 'handoff' / 'index.html'), text)
        self.assertIn('AI-DLC draft package — ZIP — ' + str(Path(root) / 'packages' / 'guided-draft' / 'ai-dlc-draft.zip'), text)
        self.assertIn('Handoff records — JSON and Markdown — ', text)

    def test_approved_package_names_the_zip_and_its_folder(self):
        ui = self.ui({'stage':'PACKAGED', 'package':{'path':'packages/package-abc.zip'}},
                     ['continue', 'functional-parity', 'v1', 'java', 'none'])
        lines = self.said(ui)
        with tempfile.TemporaryDirectory() as root, patch('reframe_setup.workspace', return_value=Path(root)):
            run(ui)
        text = '\n'.join(lines)
        self.assertIn('AI-DLC package (awaiting acceptance) — ZIP — ' + str(Path(root) / 'packages' / 'package-abc.zip'), text)
        self.assertIn('Package files — HTML, JSON, and Markdown — ' + str(Path(root) / 'packages' / 'package-abc'), text)

    def test_initial_flow_blocker_stays_in_console(self):
        from pilot import Blocked
        ui = Terminal(console=Console(file=io.StringIO()), demo=True)
        ui.session = Mock()
        ui.session.prompt.side_effect = EOFError
        with patch.object(ui, 'dispatch', side_effect=Blocked('Example blocker')):
            self.assertEqual(ui.run(initial='flow'), 0)
