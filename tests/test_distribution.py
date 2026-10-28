import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('dpe_router', ROOT / 'scripts/dpe.py')
dpe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dpe)

class DistributionTest(unittest.TestCase):
    def test_complete_catalogue_and_valid_aliases(self):
        result = dpe.validate(ROOT)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['library_skills'], 423)
        rows = dpe.catalogue(ROOT)
        self.assertEqual(len({x['name'] for x in rows}), len(rows))

    def test_data_migration_routes_domain_and_e2e_without_ui_gate(self):
        result = dpe.search(ROOT, 'Snowflake SQL ADF outbound migration E2E')
        self.assertEqual(result['primary'], 'dpe-data-pipelines')
        self.assertIn('dpe-e2e-review', result['complements'])
        self.assertNotIn('dpe-quality-ui', result['complements'])

    def test_pull_request_routes_review_not_submission(self):
        result = dpe.search(ROOT, 'review this pull request')
        self.assertEqual(result['primary'], 'dpe-rigorous-code-review')

    def test_quality_scope_tracks_requested_artifact(self):
        prose = dpe.search(ROOT, 'improve Confluence documentation')
        self.assertIn('dpe-quality-copywriting', prose['complements'])
        self.assertNotIn('dpe-quality-ui', prose['complements'])
        ui = dpe.search(ROOT, 'responsive website accessibility')
        self.assertIn('dpe-quality-layoutmobile', ui['complements'])
        self.assertIn('dpe-quality-human', ui['complements'])

    def test_exact_skill_and_alias_select_real_artifact(self):
        self.assertEqual(dpe.search(ROOT, 'dpe-data-pipelines')['primary'], 'dpe-data-pipelines')
        aliases = json.loads((ROOT / 'skills/aliases.json').read_text())['aliases']
        for alias, target in aliases.items():
            with self.subTest(alias=alias):
                self.assertEqual(dpe.search(ROOT, alias)['primary'], target)
                self.assertTrue((ROOT / 'skills' / target / 'SKILL.md').is_file())

    def test_unknown_request_does_not_fabricate_a_skill(self):
        self.assertIsNone(dpe.search(ROOT, 'qzxwvu0123456789')['primary'])

    def test_install_is_scoped_and_preserves_previous_entry(self):
        with tempfile.TemporaryDirectory(prefix='dpe skills ') as tmp:
            base = Path(tmp)
            global_file = base / 'AGENTS.md'; global_file.write_text('User rules remain unchanged')
            entry = base / 'skills/dpe-skills'
            entry.mkdir(parents=True)
            previous = entry / 'SKILL.md'; previous.write_text('previous user entry')
            unrelated = entry / 'user-note.txt'; unrelated.write_text('keep')
            result = dpe.install(ROOT, entry)
            self.assertEqual((entry / 'SKILL.md').read_bytes(), (ROOT / 'SKILL.md').read_bytes())
            self.assertEqual((entry / 'references/library-root.txt').read_text().strip(), str(ROOT.resolve()))
            self.assertEqual(global_file.read_text(), 'User rules remain unchanged')
            self.assertEqual(unrelated.read_text(), 'keep')
            self.assertFalse(result['hooks_enabled'])
            self.assertEqual((Path(result['backup']) / 'SKILL.md').read_text(), 'previous user entry')
            self.assertFalse((base / 'hooks.json').exists())

    def test_install_rejects_destination_inside_library(self):
        with self.assertRaises(ValueError): dpe.install(ROOT, ROOT / 'skills/dpe-skills')

    def test_validator_catches_missing_alias_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'skills/minimal').mkdir(parents=True)
            (root / 'skills/minimal/SKILL.md').write_text('---\nname: minimal\ndescription: test\n---\n')
            (root / 'skills/aliases.json').write_text('{"aliases":{"valid":"missing"}}')
            result = dpe.validate(root)
            self.assertEqual(result['status'], 'FAIL')
            self.assertTrue(any('missing' in e for e in result['errors']))

if __name__ == '__main__': unittest.main()
