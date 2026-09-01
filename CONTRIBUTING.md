# Contributing a workflow

Thank you for helping people start useful workflows without building one from
scratch.

## Before opening a pull request

1. Read the [Flow Captain authoring guide](https://www.chendoom.co.uk/flow-captain/authoring).
2. Create one JSON document using `chendoom-workflow` schema version 1.
3. Use lower-case kebab-case IDs and a short lower-case kebab-case filename.
4. Put the document in `workflows/`.
5. Add one entry to `library-v1.json`; keep entries ordered by title.
6. Run `python3 scripts/check_library.py`.
7. Import the JSON into Flow Captain and confirm that it opens in the visual
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

Do not place a download URL inside a workflow document. Flow Captain resolves
the path from the reviewed catalogue and then validates the downloaded JSON
locally.
