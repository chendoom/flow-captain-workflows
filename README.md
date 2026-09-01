# Flow Captain Workflow Library

This is the public, community-maintained library of workflow definitions for
[Flow Captain](https://www.chendoom.co.uk/flow-captain).

People using Flow Captain can browse this library in the app, review a
workflow visually, adapt it, and save it as one of their own workflows. Every
download is validated by Flow Captain before it can be saved or run.

## Included workflows

- **Borrowed Item** — record an item being lent, returned, and acknowledged.
- **Borrowed Vehicle** — coordinate collection, use, return, and condition
  notes.
- **Delivery Tracking** — follow a delivery through collection and confirmed
  receipt.
- **Document Review** — approve a document or return it for changes.
- **Equipment Inspection** — inspect equipment and repeat the check after
  repairs.
- **Event RSVP** — invite a guest and acknowledge their response.
- **Holiday Request** — request time away for approval by a manager.
- **Home Repair** — report a problem, track its repair, and confirm the result.
- **Household Chore** — assign a task, check it, and request another attempt if
  needed.
- **Pet Care Handover** — share care instructions and confirm the pet's return.
- **Purchase Approval** — approve, reject, or request changes to a purchase.
- **Shared Shopping List** — assign shopping, handle unavailable items, and
  confirm completion.

The app reads [`library-v1.json`](library-v1.json). The workflow documents are
in [`workflows/`](workflows/).

## Share a workflow

Please read [CONTRIBUTING.md](CONTRIBUTING.md), add a schema-version-1 workflow
document, add its catalogue entry, and open a pull request. Contributions
should be useful, understandable, domain-neutral, and free of personal data.

The public authoring format and examples are documented in the
[Flow Captain authoring guide](https://www.chendoom.co.uk/flow-captain/authoring).

## Licence

The contents of this repository are available under the [MIT Licence](LICENSE).
