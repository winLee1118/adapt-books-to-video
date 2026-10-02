import importlib.util
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', REPO / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_full_skill_and_relative_references_are_copied(self):
        with tempfile.TemporaryDirectory() as directory:
            source = REPO / installer.NAME
            target = installer.install(source, Path(directory))
            for path in source.rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                    self.assertEqual(path.read_bytes(), (target / path.relative_to(source)).read_bytes())

    def test_existing_install_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / installer.NAME
            target.mkdir()
            sentinel = target / 'SKILL.md'
            sentinel.write_text('existing user version', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                installer.install(REPO / installer.NAME, Path(directory))
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'existing user version')

    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory) / 'new' / 'skills'
            target = installer.install(REPO / installer.NAME, parent, True)
            self.assertEqual(target.name, installer.NAME)
            self.assertFalse(parent.exists())

    def test_missing_entrypoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                installer.install(Path(directory), Path(directory) / 'dest')


if __name__ == '__main__':
    unittest.main()
