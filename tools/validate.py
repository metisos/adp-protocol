#!/usr/bin/env python3
"""
Validate agent manifests against the ADP v2.0 JSON Schema.
"""
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator
from typing import List, Tuple

def load_schema() -> dict:
    """Load the ADP v2.0 JSON Schema."""
    schema_path = Path(__file__).parent.parent.parent / "shared" / "adp-spec.json"
    with open(schema_path, 'r') as f:
        return json.load(f)

def load_manifest(filepath: Path) -> dict:
    """Load a manifest JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def validate_manifest(manifest: dict, schema: dict) -> Tuple[bool, List[str]]:
    """
    Validate a manifest against the schema.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    validator = Draft7Validator(schema)
    errors = []

    for error in validator.iter_errors(manifest):
        error_path = " -> ".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"  ❌ {error_path}: {error.message}")

    return len(errors) == 0, errors

def main():
    """Validate all example manifests."""
    schema = load_schema()
    examples_dir = Path(__file__).parent.parent.parent / "examples"

    print("🔍 ADP v2.0 Manifest Validator")
    print("=" * 60)
    print()

    manifests = list(examples_dir.glob("*.json"))
    if not manifests:
        print("⚠️  No manifest files found in examples/")
        sys.exit(1)

    all_valid = True
    results = []

    for manifest_path in sorted(manifests):
        print(f"Validating: {manifest_path.name}")

        try:
            manifest = load_manifest(manifest_path)
            is_valid, errors = validate_manifest(manifest, schema)

            if is_valid:
                print(f"  ✅ Valid")
                results.append((manifest_path.name, True, []))
            else:
                print(f"  ❌ Invalid ({len(errors)} errors)")
                for error in errors:
                    print(error)
                results.append((manifest_path.name, False, errors))
                all_valid = False

        except json.JSONDecodeError as e:
            print(f"  ❌ JSON Parse Error: {e}")
            results.append((manifest_path.name, False, [f"JSON Parse Error: {e}"]))
            all_valid = False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append((manifest_path.name, False, [f"Error: {e}"]))
            all_valid = False

        print()

    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)

    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count

    print(f"Total manifests: {len(results)}")
    print(f"✅ Valid: {valid_count}")
    print(f"❌ Invalid: {invalid_count}")

    if all_valid:
        print("\n🎉 All manifests are valid!")
        sys.exit(0)
    else:
        print("\n⚠️  Some manifests have validation errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
