#!/usr/bin/env python3
"""Read-only release checks. PASS here does not certify visual quality."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def validate(data, root):
    root = Path(root).resolve()
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    def file_ok(relative, digest=None):
        if not isinstance(relative, str) or not relative:
            errors.append('Missing file path')
            return False
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            errors.append('File outside project: ' + relative)
            return False
        if not path.is_file():
            errors.append('Missing file: ' + relative)
            return False
        if digest is not None:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            require(actual == digest, 'Hash mismatch: ' + relative)
            return actual == digest
        return True

    require(data.get('schema_version') == 2, 'schema_version must be 2')
    req = data.get('requirements', {})
    require(req.get('aspect_ratio') == '16:9', 'Final aspect ratio must be 16:9')
    require(req.get('max_generation_seconds') == 15, 'Generation ceiling must be 15')
    for path in data.get('documents', {}).values():
        file_ok(path)

    def index(items, label):
        result = {}
        for item in items:
            key = item.get('id')
            require(isinstance(key, str) and bool(key), label + ' missing id')
            require(key not in result, label + ' duplicate id: ' + str(key))
            result[key] = item
        return result

    assets = index(data.get('assets', []), 'Asset')
    jobs = index(data.get('jobs', []), 'Job')
    for key, asset in assets.items():
        for field, allowed in (
            ('evidence_status', {'PASS', 'HOLD', 'CONFLICT'}),
            ('generation_status', {'PLANNED', 'PROMPT_ONLY', 'GENERATED'}),
            ('qa_status', {'PENDING', 'PASS', 'FAIL'}),
            ('use_status', {'ACTIVE', 'SUPERSEDED', 'BLOCKED'}),
        ):
            require(asset.get(field) in allowed, str(key) + ': invalid ' + field)
        if asset.get('generation_status') == 'GENERATED':
            require(bool(asset.get('sha256')), str(key) + ': missing hash')
            file_ok(asset.get('path'), asset.get('sha256'))
        else:
            require(asset.get('qa_status') != 'PASS', str(key) + ': ungenerated asset cannot pass visual QA')
        if asset.get('origin') == 'TEMPORARY_CROP':
            parent = assets.get(asset.get('parent_id'))
            require(parent is not None, str(key) + ': crop parent missing')
            if parent:
                require(asset.get('parent_sha256') == parent.get('sha256') and bool(parent.get('sha256')), str(key) + ': stale crop parent')
            box = asset.get('crop_xywh', [])
            require(len(box) == 4 and all(number(x) for x in box) and min(box[:2]) >= 0 and min(box[2:]) > 0, str(key) + ': invalid crop region')

    def approved_asset(key):
        a = assets.get(key, {})
        return (a.get('evidence_status') == 'PASS' and a.get('generation_status') == 'GENERATED'
                and a.get('qa_status') == 'PASS' and a.get('use_status') == 'ACTIVE')

    def input_lineage_ok(key, seen=None):
        seen = set() if seen is None else seen
        if key in seen:
            return False
        seen.add(key)
        asset = assets.get(key, {})
        if asset.get('origin') in {'INTERNAL_PREVIS', 'INTERNAL_QA'} or asset.get('role') in {'PREVISUALIZATION_ONLY', 'GEOMETRY_QA'}:
            return False
        if not approved_asset(key):
            return False
        if asset.get('origin') == 'TEMPORARY_CROP':
            return input_lineage_ok(asset.get('parent_id'), seen)
        return True

    for key, job in jobs.items():
        status = job.get('status')
        require(status in {'PLANNED', 'READY', 'SUBMITTED', 'GENERATED', 'APPROVED', 'REJECTED'}, str(key) + ': invalid job status')
        duration = job.get('duration_seconds')
        require(number(duration) and 0 < duration <= 15, str(key) + ': duration must be finite and within (0,15]')
        mode = job.get('mode')
        require(mode in {'SINGLE_SHOT', 'NATIVE_MULTISHOT'}, str(key) + ': invalid packaging mode')
        shots = job.get('shots', [])
        require(bool(shots), str(key) + ': no cinematic shots')
        if mode == 'SINGLE_SHOT':
            require(len(shots) == 1, str(key) + ': SINGLE_SHOT has multiple shots')
        edge = 0
        for shot in shots:
            start, end = shot.get('start'), shot.get('end')
            valid = number(start) and number(end)
            require(valid, str(key) + ': nonfinite shot time')
            if valid:
                require(abs(start-edge) < .001 and end > start, str(key) + ': shot gap, overlap or reversed interval')
                edge = end
        if number(duration):
            require(abs(edge-duration) < .001, str(key) + ': shot timeline does not cover duration')
        active = status in {'READY', 'SUBMITTED', 'GENERATED', 'APPROVED'}
        if active:
            require(bool(job.get('model')) and bool(job.get('surface')), str(key) + ': model/surface missing')
            file_ok(job.get('capability_record'))
            require(bool(job.get('prompt_sha256')), str(key) + ': prompt hash missing')
            file_ok(job.get('prompt_path'), job.get('prompt_sha256'))
            require(bool(job.get('expected_end_state')), str(key) + ': expected end state missing')
        for asset_id in job.get('input_ids', []):
            a = assets.get(asset_id)
            require(a is not None, str(key) + ': input missing ' + str(asset_id))
            if a:
                forbidden = a.get('origin') in {'INTERNAL_PREVIS', 'INTERNAL_QA'} or a.get('role') in {'PREVISUALIZATION_ONLY', 'GEOMETRY_QA'}
                require(not forbidden, str(key) + ': prohibited process input ' + str(asset_id))
                if active:
                    require(approved_asset(asset_id), str(key) + ': input not approved/active ' + str(asset_id))
                    require(input_lineage_ok(asset_id), str(key) + ': forbidden or stale input lineage ' + str(asset_id))
        for dep in job.get('depends_on', []):
            require(dep in jobs, str(key) + ': dependency missing')
            if active:
                require(jobs.get(dep, {}).get('status') == 'APPROVED', str(key) + ': dependency not approved')
        if status == 'APPROVED':
            require(approved_asset(job.get('result_asset_id')), str(key) + ': approved result missing')
            require(bool(job.get('actual_end_state')), str(key) + ': actual end state missing')
            file_ok(job.get('review_path'))
            actual_duration = job.get('actual_duration_seconds')
            require(number(actual_duration) and 0 < actual_duration <= 15, str(key) + ': actual duration missing or exceeds ceiling')

    visiting, visited = set(), set()
    def visit(key):
        if key in visiting:
            errors.append('Cyclic job dependency: ' + str(key))
            return
        if key in visited or key not in jobs:
            return
        visiting.add(key)
        for dep in jobs[key].get('depends_on', []):
            visit(dep)
        visiting.remove(key)
        visited.add(key)
    for key in jobs:
        visit(key)

    for segment in data.get('edit_segments', []):
        job = jobs.get(segment.get('job_id'), {})
        require(job.get('status') == 'APPROVED', 'Edit uses unapproved job')
        a, b, t = segment.get('in'), segment.get('out'), segment.get('timeline_start')
        duration = job.get('actual_duration_seconds')
        require(all(number(x) for x in (a,b,t,duration)) and 0 <= a < b <= duration and t >= 0, 'Invalid edit interval')
    for bridge in data.get('bridges', []):
        require(bridge.get('from_job') in jobs and bridge.get('to_job') in jobs, 'Bridge job missing')
        if bridge.get('status') == 'PASS':
            require(all(jobs.get(bridge.get(k), {}).get('status') == 'APPROVED' for k in ('from_job','to_job')), 'Bridge uses unapproved result')
            file_ok(bridge.get('review_path'))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('release', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.release.read_text(encoding='utf-8-sig'))
        errors = validate(data, args.release.parent)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(json.dumps({'status': 'INVALID', 'errors': [str(exc)]}, ensure_ascii=False))
        return 1
    status = 'INVALID' if errors else ('STRUCTURE_OK' if data.get('jobs') else 'SCAFFOLD_ONLY')
    print(json.dumps({'status': status, 'errors': errors, 'visual_quality_verified': False}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
