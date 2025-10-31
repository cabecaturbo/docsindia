#!/usr/bin/env python3
"""Fix YAML templates by using single quotes for regex patterns."""

import re
import yaml
from pathlib import Path

def fix_template(path: Path):
    """Fix regex patterns by using single quotes."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_patterns = False
    
    for line in lines:
        if 'patterns:' in line:
            in_patterns = True
            fixed_lines.append(line)
            continue
        elif in_patterns:
            # Check if this is a pattern line (starts with - and has quotes)
            if line.strip().startswith('-') and '"' in line:
                # Replace double quotes with single quotes
                fixed_line = line.replace('"', "'")
                fixed_lines.append(fixed_line)
                continue
            elif line.strip() and not line.strip().startswith('-'):
                # End of patterns section
                in_patterns = False
        
        fixed_lines.append(line)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

if __name__ == '__main__':
    templates_dir = Path(__file__).parent
    for template_file in templates_dir.glob('*.yaml'):
        if 'fix' not in template_file.name:
            print(f"Fixing {template_file.name}...")
            fix_template(template_file)

