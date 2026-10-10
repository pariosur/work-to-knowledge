import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('loop_state', ROOT / 'scripts/loop_state.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        (self.base/'work').mkdir()
        self.c = json.loads((ROOT / 'assets/config.example.json').read_text())
        self.c['enabled'] = True
        self.c['scope']['roots'] = ['work']
        self.ctx = {'roots': [str(self.base/'work')], 'topics': [], 'scope_known': True, 'no_record': False}
    def allows(self, c=None, ctx=None):
        return m.gate(c or self.c, ctx or self.ctx, self.base)
    def test_selected_and_path_boundary(self):
        self.assertTrue(self.allows())
        self.ctx['roots'] = [str(self.base/'work-other')]
        self.assertFalse(self.allows())
    def test_all_touched_roots_must_match(self):
        self.ctx['roots'].append(str(self.base/'unselected'))
        self.assertFalse(self.allows())
    def test_nonexistent_context_skips(self):
        (self.base/'work').rmdir()
        self.assertFalse(self.allows())
    def test_project_validation(self):
        self.c['scope']['mode'] = 'project'
        self.assertTrue(self.allows())
        self.c['scope']['roots'].append('another')
        self.assertFalse(self.allows())
    def test_global_exclusions_win_over_topic(self):
        self.c['scope'].update(mode='global', roots=[], exclude_topics=['private'])
        self.assertTrue(self.allows())
        self.ctx['topics'] = ['private']
        self.assertFalse(self.allows())
    def test_selected_topic_and_excluded_root(self):
        self.c['scope'].update(roots=[], topics=['research'], exclude_roots=['work'])
        self.ctx['topics'] = ['research']
        self.assertFalse(self.allows())
        self.ctx['roots'] = []
        self.assertTrue(self.allows())
    def test_symlink_cannot_escape_exclusion(self):
        (self.base/'private').mkdir()
        (self.base/'work').rmdir()
        (self.base/'work').symlink_to(self.base/'private', target_is_directory=True)
        self.c['scope']['exclude_roots'] = ['private']
        self.assertFalse(self.allows())
    def test_temporary_override_and_ambiguity(self):
        self.ctx['no_record'] = True
        self.assertFalse(self.allows())
        self.ctx['no_record'] = False
        self.ctx['scope_known'] = False
        self.assertFalse(self.allows())
    def test_missing_context_disabled_invalid(self):
        self.assertFalse(m.gate(self.c, {}, self.base))
        self.c['enabled'] = False
        self.assertFalse(self.allows())
        self.c['enabled'] = 'yes'
        self.assertFalse(self.allows())
    def test_config_change_takes_effect(self):
        self.assertTrue(self.allows())
        self.c['scope']['exclude_roots'] = ['work']
        self.assertFalse(self.allows())
    def test_episode_dedup_order_and_task_identity(self):
        self.assertEqual(m.episode_id('t', ['e2','e1','e1']), m.episode_id('t', ['e1','e2']))
        self.assertNotEqual(m.episode_id('t', ['e1']), m.episode_id('other', ['e1']))
    def test_prepared_and_committed_both_reserve(self):
        for status in ['prepared', 'committed']:
            state = {'version':1, 'episodes':{'id':{'status':status,'events':['e1','e2']}}}
            self.assertEqual(m.unreserved(state, ['e1','e2','e3','e3']), ['e3'])
    def test_corrupt_state_does_not_reset(self):
        with self.assertRaises(ValueError): m.unreserved({}, ['e1'])
        with self.assertRaises(ValueError): m.unreserved({'version':1,'episodes':{'id':{'status':'bad','events':[]}}}, ['e1'])
    def test_gate_cli_is_read_only_and_fails_closed(self):
        config, ctx = self.base/'config.json', self.base/'context.json'
        config.write_text(json.dumps(self.c))
        self.ctx['no_record'] = True
        ctx.write_text(json.dumps(self.ctx))
        before = {str(p):p.read_bytes() for p in self.base.iterdir() if p.is_file()}
        result = subprocess.run([sys.executable, str(ROOT/'scripts/loop_state.py'), 'gate',str(config),str(ctx)],capture_output=True,text=True,check=True)
        self.assertEqual(result.stdout.strip(), 'skip')
        self.assertEqual(before, {str(p):p.read_bytes() for p in self.base.iterdir() if p.is_file()})
        config.write_text('{broken')
        result = subprocess.run([sys.executable, str(ROOT/'scripts/loop_state.py'),'gate',str(config),str(ctx)],capture_output=True,text=True,check=True)
        self.assertEqual(result.stdout.strip(), 'skip')
    def test_existing_roadmap_requires_path(self):
        self.c['learning']['roadmap_mode']='existing'
        self.assertFalse(self.allows())
        self.c['learning']['existing_path']='roadmap.md'
        self.assertTrue(self.allows())

if __name__ == '__main__': unittest.main()
