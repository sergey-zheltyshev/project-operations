import unittest
from dataclasses import replace
from operations import WorkItem, checkpoints, project_attention, transition


def item(**changes):
    data=dict(id='W-1',project='Example',title='Check output',workflow='ready',attention='today',source='repo://example',next_action='Run acceptance scenario')
    return WorkItem(**{**data,**changes})


class PolicyTests(unittest.TestCase):
    def test_projection_preserves_canonical_identity_and_does_not_change_workflow(self):
        work=item()
        view=project_attention([work])
        self.assertEqual(view['views']['today'][0]['id'],work.id)
        self.assertEqual(work.workflow,'ready')

    def test_blocker_requires_concrete_dependency(self):
        with self.assertRaises(ValueError):
            item(attention='blocked')

    def test_done_requires_acceptance(self):
        with self.assertRaises(ValueError):
            item(workflow='done')
        with self.assertRaises(ValueError):
            transition(item(workflow='review'),'done')

    def test_verified_completion_clears_global_attention(self):
        complete=transition(item(workflow='review'),'done',acceptance='AC-01 passed')
        self.assertEqual(complete.attention,'none')
        self.assertFalse(project_attention([complete])['views']['today'])

    def test_invalid_jump_is_rejected(self):
        with self.assertRaises(ValueError):
            transition(item(workflow='backlog'),'done',acceptance='bypass')

    def test_capacity_is_signal_not_silent_truncation(self):
        view=project_attention([item(id=f'W-{i}') for i in range(4)])
        self.assertTrue(view['capacity']['over_limit'])
        self.assertEqual(len(view['views']['today']),4)

    def test_duplicate_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            project_attention([item(),item()])

    def test_recovery_checkpoint_has_next_action_and_source(self):
        checkpoint=checkpoints([item()])[0]
        self.assertEqual(checkpoint['resume_from'][0]['source'],'repo://example')
        self.assertEqual(checkpoint['resume_from'][0]['next_action'],'Run acceptance scenario')
