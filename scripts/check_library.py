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

MEMBER_ID = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
DEFINITION_PATH = re.compile(r"^[a-z0-9][a-z0-9._-]*(?:/[a-z0-9][a-z0-9._-]*)*\.json$")

plan_entries = catalogue.get("plans", [])
assert plan_entries == sorted(plan_entries, key=lambda entry: entry["title"].casefold())
seen_plan_ids = set()
referenced_plans = set()
plan_only_workflows = set()
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
    plan = document["plan"]
    assert plan["name"] == entry["title"], path
    if document["schemaVersion"] == 1:
        # Version 1 names a Plan that comes with the app, by identity and version.
        assert plan["id"] and plan["version"] and plan["name"], path
        assert plan["id"] == entry["id"], path
        workflow_ids = [workflow["id"] for workflow in plan["workflows"]]
        assert len(workflow_ids) == len(set(workflow_ids)), path
        known = set(workflow_ids)
        for workflow in plan["workflows"]:
            assert set(workflow.get("after", [])).issubset(known), path
        continue

    # Version 2 carries the Plan: its workflows are documents in this library.
    assert document["schemaVersion"] == 2, path
    assert "workflow-plan-v2" in capabilities, entry["id"]
    members = plan["workflows"]
    assert 2 <= len(members) <= 12, path
    member_ids = [member["id"] for member in members]
    assert all(MEMBER_ID.fullmatch(member_id) for member_id in member_ids), path
    assert len(member_ids) == len(set(member_ids)), path
    before = None
    for index, member in enumerate(members):
        definition_path = member["definitionPath"]
        assert DEFINITION_PATH.fullmatch(definition_path), (path, definition_path)
        child_path = ROOT / definition_path
        assert child_path.is_file(), (path, definition_path)
        assert child_path.resolve().is_relative_to(ROOT.resolve()), (path, definition_path)
        if not child_path.resolve().is_relative_to((ROOT / "workflows").resolve()):
            plan_only_workflows.add(child_path.resolve())
        child_document = load(child_path)
        assert child_document["format"] == "chendoom-workflow", child_path
        child_version = child_document["schemaVersion"]
        assert child_version in {1, 2, 3, 4, 5}, child_path
        if child_version >= 2:
            assert f"authoring-schema-v{child_version}" in capabilities, (entry["id"], definition_path)
        child = child_document["workflow"]
        start = next((action for action in child["actions"] if action["id"] == member["startActionId"]), None)
        assert start is not None, (path, member["startActionId"])
        assert any(route["from"] == "start" for route in start["paths"]), (path, member["startActionId"])
        role_bindings = member.get("roleBindings", [])
        input_bindings = member.get("inputBindings", [])
        if index == 0:
            assert "roleBindings" not in member and "inputBindings" not in member, path
        else:
            filled_roles = [binding["toRoleId"] for binding in role_bindings]
            assert len(filled_roles) == len(set(filled_roles)), (path, member["id"])
            filled_inputs = [binding["toInputId"] for binding in input_bindings]
            assert len(filled_inputs) == len(set(filled_inputs)), (path, member["id"])
            roles = {role["id"] for role in child["roles"]}
            roles_before = {role["id"] for role in before["roles"]}
            for binding in role_bindings:
                assert binding["fromRoleId"] in roles_before, (path, binding)
                assert binding["toRoleId"] in roles, (path, binding)
            inputs = {field["id"] for field in start.get("payload", [])}
            fields_before = {field["id"] for field in before.get("data", [])}
            for binding in input_bindings:
                assert binding["fromFieldId"] in fields_before, (path, binding)
                assert binding["toInputId"] in inputs, (path, binding)
        before = child

available_plans = {path.resolve() for path in (ROOT / "plans").glob("*.json")}
assert referenced_plans == available_plans, "Every Plan file must appear exactly once in the catalogue"
# A workflow written only for a Plan lives in a folder beside it, such as plans/example/first.json.
available_plan_only = {path.resolve() for path in (ROOT / "plans").glob("*/*.json")}
assert plan_only_workflows == available_plan_only, "Every workflow beside a Plan must be used by one"

print(f"Checked {len(entries)} workflow definitions and {len(plan_entries)} workflow plans")
