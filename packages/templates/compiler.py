#!/usr/bin/env python3
"""YAML template compiler to validated JSON for extraction engines."""

import json
import re
import yaml
from pathlib import Path
from typing import Any, Dict, List


def load_template(path: Path) -> Dict[str, Any]:
    """Load and parse a YAML template."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_template(tpl: Dict[str, Any]) -> List[str]:
    """Validate template structure. Returns list of errors (empty if valid)."""
    errors = []
    if "id" not in tpl:
        errors.append("Missing 'id' field")
    if "version" not in tpl:
        errors.append("Missing 'version' field")
    if "fields" not in tpl:
        errors.append("Missing 'fields' field")
    if not isinstance(tpl.get("fields"), dict):
        errors.append("'fields' must be a dictionary")
    else:
        for field_name, field_def in tpl.get("fields", {}).items():
            if "patterns" not in field_def:
                errors.append(f"Field '{field_name}' missing 'patterns'")
            elif not isinstance(field_def["patterns"], list):
                errors.append(f"Field '{field_name}' patterns must be a list")
    return errors


def compile_template(tpl: Dict[str, Any]) -> Dict[str, Any]:
    """Compile YAML template to JSON-ready extraction manifest."""
    compiled = {
        "id": tpl["id"],
        "version": tpl["version"],
        "issuers": tpl.get("issuers", []),
        "fields": {},
        "post_rules": tpl.get("post_rules", []),
        "red_flags": tpl.get("red_flags", []),
    }
    
    # Compile regex patterns for each field
    for field_name, field_def in tpl.get("fields", {}).items():
        patterns = []
        for pattern_str in field_def.get("patterns", []):
            try:
                # Validate regex
                re.compile(pattern_str)
                patterns.append(pattern_str)
            except re.error as e:
                raise ValueError(f"Invalid regex in field '{field_name}': {e}")
        
        compiled["fields"][field_name] = {
            "patterns": patterns,
            "group_name": "value"  # Default capture group name
        }
    
    return compiled


def compile_all_templates(templates_dir: Path, output_dir: Path) -> None:
    """Compile all YAML templates to JSON in output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    templates = list(templates_dir.glob("*.yaml"))
    
    compiled_templates = []
    errors = []
    
    for tpl_path in templates:
        try:
            tpl = load_template(tpl_path)
            validation_errors = validate_template(tpl)
            if validation_errors:
                errors.extend([f"{tpl_path.name}: {e}" for e in validation_errors])
                continue
            
            compiled = compile_template(tpl)
            output_path = output_dir / f"{tpl['id']}.json"
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(compiled, f, indent=2, ensure_ascii=False)
            
            compiled_templates.append({
                "id": compiled["id"],
                "version": compiled["version"],
                "issuers": compiled["issuers"]
            })
            
        except Exception as e:
            errors.append(f"{tpl_path.name}: {e}")
    
    # Write index
    index_path = output_dir / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"docTypes": compiled_templates}, f, indent=2, ensure_ascii=False)
    
    if errors:
        print("Errors during compilation:")
        for error in errors:
            print(f"  - {error}")
        raise ValueError(f"Compilation failed with {len(errors)} error(s)")
    
    print(f"Compiled {len(compiled_templates)} templates successfully")


if __name__ == "__main__":
    templates_dir = Path(__file__).parent
    output_dir = templates_dir / "compiled"
    compile_all_templates(templates_dir, output_dir)

