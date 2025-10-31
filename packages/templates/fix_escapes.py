#!/usr/bin/env python3
"""Fix regex escape sequences in YAML templates."""

import re
import yaml
from pathlib import Path

def fix_template(path: Path):
    """Fix regex patterns in a template file."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace unescaped \s, \d, etc. with double backslashes
    # But keep \n, \t, \r as they are valid YAML escapes
    patterns_to_fix = [
        (r'(?<!\\)\\(?![nrt"\'\\])', r'\\\\'),  # Escape single backslashes except valid ones
    ]
    
    # Actually, simpler: replace \s, \d, \., \-, etc. patterns with double backslashes
    # Look for regex patterns inside quoted strings
    lines = content.split('\n')
    fixed_lines = []
    in_patterns = False
    current_indent = 0
    
    for line in lines:
        if 'patterns:' in line:
            in_patterns = True
            fixed_lines.append(line)
            current_indent = len(line) - len(line.lstrip())
            continue
        elif in_patterns and line.strip().startswith('-'):
            # This is a pattern line
            # Find the regex pattern part (after the quote)
            if '"' in line:
                parts = line.split('"', 1)
                if len(parts) > 1:
                    pattern = parts[1].rstrip('"')
                    # Double all backslashes except those before n, t, r
                    fixed_pattern = re.sub(r'\\(?![nrt"\'\\])', r'\\\\', pattern)
                    fixed_line = parts[0] + '"' + fixed_pattern + '"'
                    fixed_lines.append(fixed_line)
                    continue
        elif in_patterns and (not line.strip() or len(line) - len(line.lstrip()) <= current_indent):
            in_patterns = False
        
        fixed_lines.append(line)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))

if __name__ == '__main__':
    templates_dir = Path(__file__).parent
    for template_file in templates_dir.glob('*.yaml'):
        if template_file.name != 'fix_escapes.py':
            print(f"Fixing {template_file.name}...")
            fix_template(template_file)

