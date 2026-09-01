#!/usr/bin/env python3
"""Fast repository checks; Flow Captain remains the semantic validator."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "library-v1.json"
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicates)


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate property {key!r}")
        result[key] = value
    return result


catalogue = load(CATALOGUE)
assert catalogue["format"] == "flow-captain-workflow-library"
assert catalogue["schemaVersion"] == 1
entries = catalogue["workflows"]
assert entries == sorted(entries, key=lambda entry: entry["title"].casefold())

seen = set()
referenced = set()
for entry in entries:
    assert ID.fullmatch(entry["id"]), entry["id"]
    assert entry["id"] not in seen, entry["id"]
    seen.add(entry["id"])
    path = ROOT / entry["definitionPath"]
    assert path.is_file(), path
    assert path.resolve().is_relative_to((ROOT / "workflows").resolve()), path
    referenced.add(path.resolve())
    document = load(path)
    assert document["format"] == "chendoom-workflow", path
    assert document["schemaVersion"] == 1, path
    assert document["workflow"]["name"] == entry["title"], path

available = {path.resolve() for path in (ROOT / "workflows").glob("*.json")}
assert referenced == available, "Every workflow file must appear exactly once in the catalogue"
print(f"Checked {len(entries)} workflow definitions")
