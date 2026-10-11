"""Offline regression checks for both native packages and the portable source."""
import importlib.util
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync_plugin', ROOT / 'scripts/sync_plugin.py')
sync_plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_plugin)


def read(path):
    return json.loads((ROOT / path).read_text())


class PluginPackagingTests(unittest.TestCase):
    def test_generated_bundle_matches(self):
        sync_plugin.sync(check=True)

    def test_manifest_identity_and_versions_agree(self):
        manifests = [read(p) for p in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json')]
        for manifest in manifests:
            self.assertEqual(manifest['name'], 'work-to-knowledge')
            self.assertRegex(manifest['version'], r'^\d+\.\d+\.\d+$')
            self.assertEqual(manifest['version'], manifests[0]['version'])
            self.assertEqual(manifest['license'], 'MIT')
            self.assertEqual(manifest['author']['name'], 'Pablo Ríos')
            self.assertTrue(manifest['description'])
            self.assertNotIn('hooks', manifest)
            self.assertNotIn('mcpServers', manifest)

    def test_marketplaces_resolve_same_package(self):
        codex = read('.agents/plugins/marketplace.json')
        claude = read('.claude-plugin/marketplace.json')
        self.assertEqual(codex['name'], claude['name'])
        self.assertTrue(claude['owner']['name'])
        for marketplace in (codex, claude):
            self.assertEqual(len(marketplace['plugins']), 1)
            entry = marketplace['plugins'][0]
            self.assertEqual(entry['name'], 'work-to-knowledge')
            source = entry['source']
            path = source['path'] if isinstance(source, dict) else source
            self.assertTrue(path.startswith('./'))
            self.assertNotIn('..', Path(path).parts)
            self.assertEqual((ROOT / path).resolve(), ROOT)
        self.assertEqual(codex['plugins'][0]['policy'], {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'})
        self.assertEqual(codex['plugins'][0]['category'], 'Productivity')

    def test_one_workflow_and_explicit_setup(self):
        skills = sorted((ROOT / 'skills').glob('*/SKILL.md'))
        self.assertEqual([p.parent.name for p in skills], ['setup', 'work-to-knowledge'])
        for path in skills:
            text = path.read_text()
            self.assertTrue(text.startswith('---\n'))
            self.assertIn('\nname: ' + path.parent.name + '\n', text)
            self.assertIn('\ndescription: ', text)
        self.assertIn('disable-model-invocation: true', skills[0].read_text())
        self.assertIn('allow_implicit_invocation: false', (ROOT / 'skills/setup/agents/openai.yaml').read_text())
        self.assertFalse((ROOT / 'hooks').exists())
        self.assertFalse((ROOT / 'commands').exists())

    def test_onboarding_paths(self):
        root = read('plugin.json')['extensions']['com.openai']
        compat = read('.codex-plugin/plugin.json')['extensions']['com.openai']
        self.assertEqual(root['onboardingSkill'], compat['onboardingSkill'])
        self.assertEqual(root['onboardingSkill'], './skills/setup/SKILL.md')
        self.assertTrue((ROOT / root['onboardingSkill']).is_file())
        self.assertEqual(read('.codex-plugin/plugin.json')['skills'], './skills/')

    def test_bundle_links_resolve_within_plugin(self):
        # Templates and workflow intentionally contain schematic note destinations.
        for relative in ('SKILL.md', 'references/setup.md', 'references/harnesses.md', 'references/examples.md'):
            path = ROOT / 'skills/work-to-knowledge' / relative
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if urlsplit(target).scheme or target.startswith('#'):
                    continue
                resolved = (path.parent / unquote(target.split('#')[0])).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT), target)
                self.assertTrue(resolved.exists(), (relative, target))
        setup = ROOT / 'skills/setup/SKILL.md'
        for target in re.findall(r'\]\(([^)]+)\)', setup.read_text()):
            self.assertTrue((setup.parent / target).is_file(), target)

    def test_example_config_does_not_record_or_share(self):
        config = read('skills/work-to-knowledge/assets/config.example.json')
        self.assertFalse(config['enabled'])
        self.assertEqual(config['sources'], [])
        self.assertEqual(config['scope']['roots'], [])
        self.assertEqual(config['scope']['topics'], [])

    def test_preserves_portable_assets_and_license(self):
        self.assertTrue((ROOT / 'SKILL.md').is_file())
        self.assertEqual((ROOT / 'assets/work-to-knowledge-overview.png').read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
        self.assertIn('MIT License', (ROOT / 'LICENSE').read_text())

    def test_no_runtime_configuration_bundled(self):
        for path in ('.codex/config.toml', '.claude/settings.json', 'AGENTS.md', 'CLAUDE.md', '.mcp.json', 'mcp.json', '.app.json'):
            self.assertFalse((ROOT / path).exists(), path)
        self.assertFalse(any((ROOT / 'skills').rglob('*.pyc')))


if __name__ == '__main__':
    unittest.main()
