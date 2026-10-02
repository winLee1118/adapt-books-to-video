#!/usr/bin/env python3
"""Install the bundled agent skill offline without replacing existing files."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

NAME = 'adapt-books-to-video'


def install(source: Path, parent: Path, dry_run: bool = False) -> Path:
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Source must contain SKILL.md')
    target = parent.expanduser().resolve() / NAME
    if target.exists() or target.is_symlink():
        raise FileExistsError(f'Refusing to overwrite existing skill: {target}')
    if target == source.resolve() or source.resolve() in target.parents:
        raise ValueError('Installation target must be outside the source skill')
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dest', type=Path, help='Skill parent directory for any supported agent')
    group.add_argument('--project', type=Path, help='Install into PROJECT/.agents/skills')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating directories')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent / NAME
    parent = args.dest or ((args.project / '.agents' / 'skills') if args.project else Path.home() / '.agents' / 'skills')
    try:
        target = install(source, parent, args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    print(json.dumps({'status': 'DRY_RUN' if args.dry_run else 'INSTALLED', 'skill': NAME, 'path': str(target),
                      'files': sum(p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' for p in source.rglob('*'))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
