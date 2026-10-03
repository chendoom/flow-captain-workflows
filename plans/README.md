# Workflow Plans

A Plan links several workflows into one larger journey. Each workflow starts by
itself when the one before it ends, and can take people and information from it.
The workflows stay ordinary workflows: the Plan only says how they join.

## Plans in this library

- **Group Trip** ([`group-trip.json`](group-trip.json)) — suggest destinations,
  choose one, then record and split trip expenses. This Plan comes with Flow
  Captain, so its document is a version 1 manifest: it names the bundled Plan
  (version 16, with Trip Proposal 17 and Trip Expenses 19) rather than carrying
  it. The app reviews the entry and opens the Plan it already has.
- **Vehicle Loan and Check** ([`vehicle-loan-and-check.json`](vehicle-loan-and-check.json))
  — lend a vehicle, then have it inspected once it is back. This is a version 2
  document: it links [Borrowed Vehicle](../workflows/borrowed-vehicle.json) to
  [Equipment Inspection](../workflows/equipment-inspection.json). The owner
  becomes the inspection's operator, observers carry on observing, and the
  vehicle's name fills in what is to be inspected.

## Version 2: a Plan the app can add

Flow Captain downloads a version 2 Plan together with every workflow document
it names, checks them all on the device, and shows one review. Nothing is saved
until the person adds the Plan. They then own the Plan and its workflows, and
can change or delete them like any others.

```json
{
  "$schema": "../schemas/workflow-plan-v2.schema.json",
  "format": "chendoom-workflow-plan",
  "schemaVersion": 2,
  "plan": {
    "name": "Vehicle Loan and Check",
    "description": "Lend a vehicle, then have it inspected once it is back. …",
    "workflows": [
      {
        "id": "loan",
        "definitionPath": "workflows/borrowed-vehicle.json",
        "startActionId": "offer-vehicle"
      },
      {
        "id": "inspection",
        "definitionPath": "workflows/equipment-inspection.json",
        "startActionId": "request-inspection",
        "roleBindings": [
          { "fromRoleId": "owner", "toRoleId": "operator" },
          { "fromRoleId": "observer", "toRoleId": "observer" }
        ],
        "inputBindings": [
          { "fromFieldId": "vehicle", "toInputId": "equipment" }
        ]
      }
    ]
  }
}
```

- `workflows` lists the workflows in the order they run. There are at least
  two and at most twelve.
- `id` is a lower-case kebab-case name for that step, unique within the Plan.
- `definitionPath` is the workflow document, as a path from the root of this
  repository. It is never a URL. A workflow written only for a Plan goes in a
  folder beside it, such as `plans/example/first-step.json`.
- `startActionId` is the action that starts that workflow.
- `roleBindings` say who carries on: the people holding `fromRoleId` in the
  workflow before hold `toRoleId` in this one. A role nobody carries into is
  assigned when the Plan starts.
- `inputBindings` say what is brought forward: the data field `fromFieldId` of
  the workflow before fills the input `toInputId` of this workflow's start
  action. An input nothing fills is asked for when the Plan starts.
- The first workflow has no bindings: there is nothing before it.

The schema is [`workflow-plan-v2.schema.json`](../schemas/workflow-plan-v2.schema.json).
It is closed: a property it does not name is an error.

## What to check before proposing a Plan

- **Every ending leads on.** The next workflow starts whenever the one before
  it ends, whatever the outcome. Choose a first workflow whose every ending
  should be followed by the next one.
- **Bring forward what is certain to be there.** Information can only fill an
  input of the same kind, and information that might be missing cannot fill an
  input that must have a value. In practice, bring forward fields the earlier
  workflow required when it started, or its record collections.
- **Record collections come from the workflow before.** A later workflow's
  record collection input cannot be typed in when the Plan starts.
- **The app is the judge.** `scripts/check_library.py` checks that every
  reference exists; Flow Captain and its engine decide whether the Plan is
  valid. Download the Plan in the app and review it before opening a pull
  request.

The catalogue entry declares `workflow-plan-v2` and the `authoring-schema-v…`
capability of each workflow it links, so an older app asks for an update
instead of trying to read it.
