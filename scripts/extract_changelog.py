#!/usr/bin/env python3
"""Extract changelog section for a specific version."""

import re
import sys

def extract_changelog(version, changelog_path='CHANGELOG.md', output_path='release-notes.md'):
    with open(changelog_path, 'r') as f:
        content = f.read()

    # Find version section - look for "## [X.Y.Z]" pattern
    # The version in changelog has format "## [2.0.0] - 2025-08-24"
    pattern = rf'(## \[{re.escape(version)}\]\s*.*?)(?=\n## \[|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        notes = match.group(1).strip()
    else:
        # Fallback: last 50 lines
        notes = '\n'.join(content.split('\n')[-50:])

    with open(output_path, 'w') as f:
        f.write(notes)
    print(f"Extracted changelog for version {version}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_changelog(sys.argv[1])
    else:
        print("Usage: extract_changelog.py <version>")
        sys.exit(1)