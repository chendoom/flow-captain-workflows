# Contributing a workflow

Thank you for helping people start useful workflows without building one from
scratch.

## Recommended: create it with AI

The easiest route is the same **Use AI** path available on Flow Captain's
Definitions screen:

1. Open the [Flow Captain AI authoring guide](https://www.chendoom.co.uk/flow-captain/authoring).
2. Give its authoring context and schema to ChatGPT, Codex, Claude, Gemini, or
   another capable AI.
3. Describe the roles, starting information, actions, outcomes, and any
   deadlines in ordinary language.
4. Ask the AI to return exactly one schema-version-2 workflow JSON document.
5. Import that JSON into Flow Captain, review the visual graph, and correct any
   validation issues before submitting it here.

AI output is only a draft. You remain responsible for reviewing the workflow
and confirming that its names, paths, permissions, and outcomes match what you
intend.

## Before opening a pull request

1. Create one JSON document using a supported `chendoom-workflow` schema,
   ideally the current version 2, through the AI-assisted route above.
2. Use lower-case kebab-case IDs and a short lower-case kebab-case filename.
3. Put the document in `workflows/`.
4. Add one entry to `library-v1.json`; keep entries ordered by title.
5. Run `python3 scripts/check_library.py`.
6. Import the JSON into Flow Captain and confirm that it opens in the visual
   editor without blocking validation errors.

## What belongs here

- A focused workflow that is useful to more than one person.
- A clear description, role names, state names, and action names.
- No personal data, account identifiers, secrets, or executable code.
- No dependency on a particular company, private system, or paid service.
- An original contribution that can be distributed under the MIT Licence.

The catalogue is curated. A valid document may still be declined when it
duplicates an existing workflow, is too specialised, or is difficult to
understand safely.

## Catalogue fields

- `id`: stable lower-case kebab-case identifier.
- `title`: short user-facing name.
- `summary`: one concise sentence.
- `author`: contributor or organisation name.
- `iconSystemName`: an SF Symbol supported by Flow Captain.
- `definitionPath`: relative path to the JSON document.
- `requiredCapabilities`: optional stable capability IDs required to understand
  the definition. Use this only for vocabulary that older Flow Captain builds
  do not support.

When an app release adds public authoring functionality, update the published
authoring contract first. A library item using that functionality must declare
its required capability. Apps that understand the catalogue metadata will ask
the user to update before downloading it; the strict document importer remains
the safety check for older apps. A breaking change to the document envelope or
existing vocabulary requires a new authoring schema version rather than a
silent change to an already published contract.

Do not place a download URL inside a workflow document. Flow Captain resolves
the path from the reviewed catalogue and then validates the downloaded JSON
locally.
