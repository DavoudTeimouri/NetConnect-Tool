#!/usr/bin/env python3
"""Extract changelog section for a single version (one release = its own notes)."""

import re
import sys

VERSION_HEADER = re.compile(r'^##\s+\[([^\]]+)\]')


def extract_changelog(version, changelog_path='CHANGELOG.md', output_path='release-notes.md'):
    with open(changelog_path, 'r') as f:
        lines = f.readlines()

    # Locate the target version header
    start = None
    for i, line in enumerate(lines):
        m = VERSION_HEADER.match(line)
        if m and m.group(1) == version:
            start = i
            break

    if start is None:
        raise SystemExit(f"ERROR: version [{version}] not found in {changelog_path}")

    # End at the next version header (or EOF) — never spill into other releases
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if VERSION_HEADER.match(lines[j]):
            end = j
            break

    notes = ''.join(lines[start:end]).strip() + '\n'

    with open(output_path, 'w') as f:
        f.write(notes)

    print(f"Extracted changelog section for v{version} ({len(notes)} chars)")
    return notes


if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_changelog(sys.argv[1])
    else:
        print("Usage: extract_changelog.py <version>")
        sys.exit(1)
