import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import generate_dashboard as dashboard


class DashboardTests(unittest.TestCase):
    def setup_project(self, root):
        (root / 'script.md').write_text('共用标题\n第一条动作\n第一条对白\n第二条动作\n', encoding='utf-8')
        (root / 'prompt.txt').write_text('动作 <script>alert(1)</script> & 声音', encoding='utf-8')
        (root / 'unassigned.md').write_text('未归属制作记录', encoding='utf-8')
        (root / '.env').write_text('PRIVATE_SECRET=do-not-display', encoding='utf-8')
        data = {'schema_version': 1, 'project_title': '工作流测试', 'shared_files': ['unassigned.md'], 'videos': [
            {'id': 'u1', 'scene_number': 2, 'video_number': 1, 'files': [
                {'path': 'script.md', 'group': 'script_breakdown', 'line_start': 2, 'line_end': 3},
                {'path': 'prompt.txt', 'group': 'prompts'}, {'path': 'future.png', 'group': 'assets'}]},
            {'id': 'u2', 'episode_number': 3, 'scene_number': 4, 'video_number': 2, 'files': [
                {'path': 'script.md', 'group': 'script_detail', 'line_start': 4, 'line_end': 4}]}]}
        self.save(root, data)
        return data

    def save(self, root, data):
        (root / 'dashboard-map.json').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def test_cli_requires_explicit_trigger_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.setup_project(root)
            result = subprocess.run([sys.executable, dashboard.__file__, '--project', str(root)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'reports').exists())

    def test_video_numbering_excerpts_safe_text_and_complete_index(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.setup_project(root)
            result = dashboard.generate(root)
            self.assertEqual(result['video_count'], 2)
            dest = root / 'reports' / 'boards'
            one = (dest / dashboard.page_name('u1')).read_text(encoding='utf-8')
            two = (dest / dashboard.page_name('u2')).read_text(encoding='utf-8')
            self.assertIn('<h1>第2场 · 第1条视频</h1>', one)
            self.assertIn('<h1>第3集 · 第4场 · 第2条视频</h1>', two)
            self.assertIn('第一条动作\n第一条对白', one)
            self.assertNotIn('第二条动作', one)
            self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', one)
            self.assertNotIn('<script>alert(1)</script>', one)
            self.assertIn('unassigned.md', one)
            self.assertIn('文件缺失／待生成', one)
            self.assertNotIn('PRIVATE_SECRET', one)
            self.assertNotIn('>.env<', one)
            self.assertEqual(result['indexed_file_count'], 4)

    def test_missing_number_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = self.setup_project(root)
            del data['videos'][0]['scene_number']
            self.save(root, data)
            with self.assertRaises(ValueError):
                dashboard.generate(root)
            self.assertFalse((root / 'reports').exists())

    def test_outside_and_private_files_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = self.setup_project(root)
            for relative in ('../private.txt', '.env'):
                data['videos'][0]['files'] = [{'path': relative}]
                self.save(root, data)
                with self.assertRaises(ValueError):
                    dashboard.generate(root)
            self.assertFalse((root / 'reports').exists())

    def test_invalid_excerpt_and_unknown_job_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = self.setup_project(root)
            data['videos'][0]['files'][0]['line_end'] = 99
            self.save(root, data)
            with self.assertRaises(ValueError):
                dashboard.generate(root)
            data['videos'][0]['files'][0]['line_end'] = 3
            data['videos'][0]['job_ids'] = ['not-recorded']
            self.save(root, data)
            with self.assertRaises(ValueError):
                dashboard.generate(root)

    def test_refresh_preserves_other_files_and_requires_owned_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.setup_project(root)
            dashboard.generate(root)
            dest = root / 'reports' / 'boards'
            sentinel = dest / 'user-note.txt'
            sentinel.write_text('keep', encoding='utf-8')
            with self.assertRaises(ValueError):
                dashboard.generate(root)
            result = dashboard.generate(root, refresh=True)
            self.assertEqual(result['indexed_file_count'], 4)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'keep')

    def test_release_jobs_and_assets_are_mapped_without_approval_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = self.setup_project(root)
            data['videos'][0]['job_ids'] = ['GEN-01']
            self.save(root, data)
            release = {'release_id': 'R004', 'jobs': [{'id': 'GEN-01', 'status': 'PLANNED',
                'prompt_path': 'prompt.txt', 'input_ids': ['ASSET-01']}],
                'assets': [{'id': 'ASSET-01', 'path': 'future.png', 'generation_status': 'PROMPT_ONLY', 'qa_status': 'PENDING'}]}
            release_path = root / 'active-release.json'
            release_path.write_text(json.dumps(release), encoding='utf-8')
            before = release_path.read_bytes()
            dashboard.generate(root)
            self.assertEqual(before, release_path.read_bytes())
            page = (root / 'reports' / 'boards' / dashboard.page_name('u1')).read_text(encoding='utf-8')
            self.assertIn('GEN-01 · PLANNED', page)
            self.assertIn('R004', page)


if __name__ == '__main__':
    unittest.main()
