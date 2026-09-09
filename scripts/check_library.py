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
    capabilities = entry.get("requiredCapabilities", [])
    assert len(capabilities) == len(set(capabilities)), entry["id"]
    assert all(ID.fullmatch(capability) for capability in capabilities), entry["id"]
    path = ROOT / entry["definitionPath"]
    assert path.is_file(), path
    assert path.resolve().is_relative_to((ROOT / "workflows").resolve()), path
    referenced.add(path.resolve())
    document = load(path)
    assert document["format"] == "chendoom-workflow", path
    schema_version = document["schemaVersion"]
    assert schema_version in {1, 2, 3, 4, 5}, path
    if schema_version >= 2:
        assert f"authoring-schema-v{schema_version}" in capabilities, entry["id"]
    assert document["workflow"]["name"] == entry["title"], path

available = {path.resolve() for path in (ROOT / "workflows").glob("*.json")}
assert referenced == available, "Every workflow file must appear exactly once in the catalogue"

plan_entries = catalogue.get("plans", [])
assert plan_entries == sorted(plan_entries, key=lambda entry: entry["title"].casefold())
seen_plan_ids = set()
referenced_plans = set()
for entry in plan_entries:
    assert ID.fullmatch(entry["id"]), entry["id"]
    assert entry["id"] not in seen_plan_ids, entry["id"]
    seen_plan_ids.add(entry["id"])
    capabilities = entry.get("requiredCapabilities", [])
    assert len(capabilities) == len(set(capabilities)), entry["id"]
    assert all(ID.fullmatch(capability) for capability in capabilities), entry["id"]
    path = ROOT / entry["definitionPath"]
    assert path.is_file(), path
    assert path.resolve().is_relative_to((ROOT / "plans").resolve()), path
    referenced_plans.add(path.resolve())
    document = load(path)
    assert document["format"] == "chendoom-workflow-plan", path
    assert document["schemaVersion"] == 1, path
    plan = document["plan"]
    assert plan["id"] and plan["version"] and plan["name"], path
    assert plan["id"] == entry["id"], path
    assert plan["name"] == entry["title"], path
    workflow_ids = [workflow["id"] for workflow in plan["workflows"]]
    assert len(workflow_ids) == len(set(workflow_ids)), path
    known = set(workflow_ids)
    for workflow in plan["workflows"]:
        assert set(workflow.get("after", [])).issubset(known), path

available_plans = {path.resolve() for path in (ROOT / "plans").glob("*.json")}
assert referenced_plans == available_plans, "Every Plan file must appear exactly once in the catalogue"

print(f"Checked {len(entries)} workflow definitions and {len(plan_entries)} workflow plans")
