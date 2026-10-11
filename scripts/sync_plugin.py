#!/usr/bin/env python3
"""Build/check the native skill bundle from the portable source; never edit user config."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'skills' / 'work-to-knowledge'
FILES = ('SKILL.md', 'LICENSE', 'assets/config.example.json', 'assets/templates.md',
         'references/setup.md', 'references/harnesses.md', 'references/workflow.md',
         'references/examples.md', 'scripts/loop_state.py')


def sync(check=False):
    expected = {Path(name) for name in FILES}
    actual = {p.relative_to(DEST) for p in DEST.rglob('*') if p.is_file()}
    extra = actual - expected
    if extra:
        raise SystemExit('Unexpected bundle files (review manually): ' + ', '.join(map(str, sorted(extra))))
    stale = []
    for name in FILES:
        src, dst = ROOT / name, DEST / name
        if not dst.exists() or src.read_bytes() != dst.read_bytes():
            stale.append(name)
            if not check:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(src.read_bytes())
    if check and stale:
        raise SystemExit('Stale bundle; run python3 scripts/sync_plugin.py: ' + ', '.join(stale))
    print('Plugin bundle matches portable source' if check else 'Plugin bundle synchronized')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    sync(parser.parse_args().check)
