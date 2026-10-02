import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from validate_release import validate


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'ref.png').write_bytes(b'test asset, not visually approved by this test')
        (self.root / 'prompt.txt').write_text('test prompt')
        (self.root / 'cap.md').write_text('test capability record')
        self.data = {
            'schema_version': 2,
            'requirements': {'aspect_ratio': '16:9', 'max_generation_seconds': 15},
            'assets': [{'id': 'A', 'path': 'ref.png', 'sha256': hashlib.sha256((self.root/'ref.png').read_bytes()).hexdigest(),
                        'origin': 'GENERATED', 'evidence_status': 'PASS', 'generation_status': 'GENERATED',
                        'qa_status': 'PASS', 'use_status': 'ACTIVE', 'role': 'IDENTITY'}],
            'jobs': [{'id': 'G1', 'status': 'READY', 'mode': 'NATIVE_MULTISHOT', 'duration_seconds': 11,
                      'model': 'test', 'surface': 'test', 'capability_record': 'cap.md',
                      'prompt_path': 'prompt.txt', 'prompt_sha256': hashlib.sha256((self.root/'prompt.txt').read_bytes()).hexdigest(),
                      'input_ids': ['A'], 'expected_end_state': 'test state',
                      'shots': [{'id': 'S1', 'start': 0, 'end': 4.2}, {'id':'S2', 'start':4.2, 'end':7}, {'id':'S3','start':7,'end':11}]}],
        }

    def test_eleven_second_three_shot_job_is_valid(self):
        self.assertEqual([], validate(self.data, self.root))

    def test_gap_and_nonfinite_duration_rejected(self):
        self.data['jobs'][0]['shots'][1]['start'] = 4.3
        self.assertTrue(any('gap' in e for e in validate(self.data, self.root)))
        self.data['jobs'][0]['duration_seconds'] = float('nan')
        self.assertTrue(any('finite' in e for e in validate(self.data, self.root)))

    def test_previs_rejected_even_if_marked_pass(self):
        self.data['assets'][0]['origin'] = 'INTERNAL_PREVIS'
        self.assertTrue(any('prohibited' in e for e in validate(self.data, self.root)))

    def test_stale_file_and_superseded_input_rejected(self):
        (self.root / 'ref.png').write_bytes(b'new version')
        self.data['assets'][0]['use_status'] = 'SUPERSEDED'
        errors = validate(self.data, self.root)
        self.assertTrue(any('Hash mismatch' in e for e in errors))
        self.assertTrue(any('not approved/active' in e for e in errors))

    def test_dependency_cycle_rejected(self):
        job = self.data['jobs'][0]
        job['status'] = 'PLANNED'
        job['depends_on'] = ['G2']
        other = copy.deepcopy(job)
        other['id'], other['depends_on'] = 'G2', ['G1']
        self.data['jobs'].append(other)
        self.assertTrue(any('Cyclic' in e for e in validate(self.data, self.root)))

    def test_prompt_ready_does_not_mean_video_approved(self):
        self.data['jobs'][0]['status'] = 'APPROVED'
        errors = validate(self.data, self.root)
        self.assertTrue(any('approved result missing' in e for e in errors))
        self.assertTrue(any('actual end state missing' in e for e in errors))

    def test_file_cannot_escape_project(self):
        self.data['assets'][0]['path'] = '../ref.png'
        self.assertTrue(any('outside project' in e for e in validate(self.data, self.root)))

    def test_crop_cannot_launder_previs_input(self):
        parent = self.data['assets'][0]
        parent['origin'] = 'INTERNAL_PREVIS'
        crop = copy.deepcopy(parent)
        crop.update(id='C', origin='TEMPORARY_CROP', parent_id='A', parent_sha256=parent['sha256'], crop_xywh=[0,0,10,10])
        self.data['assets'].append(crop)
        self.data['jobs'][0]['input_ids'] = ['C']
        self.assertTrue(any('input lineage' in e for e in validate(self.data, self.root)))


if __name__ == '__main__':
    unittest.main()
