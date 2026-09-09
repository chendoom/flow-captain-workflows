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
- **Shared Shopping List** — let everyone add, purchase, or remove items while
  retaining concurrent purchases and highlighting extras.

The app reads [`library-v1.json`](library-v1.json). The workflow documents are
in [`workflows/`](workflows/).

## Workflow Plans

Plans connect several workflows into a larger journey. The first public Plan,
**Group Trip**, covers choosing a destination and tracking shared expenses. Its
review manifest and pinned bundled versions are in [`plans/`](plans/README.md).

Travellers in that Plan do not need app accounts. An authorised Flow Captain
user can record a booking or expense for them, while the audit data still says
which signed-in actor entered it.

## Share a workflow

Please read [CONTRIBUTING.md](CONTRIBUTING.md), add a supported versioned workflow
document, add its catalogue entry, and open a pull request. Contributions
should be useful, understandable, domain-neutral, and free of personal data.

The public authoring format and examples are documented in the
[Flow Captain authoring guide](https://www.chendoom.co.uk/flow-captain/authoring).

## Licence

The contents of this repository are available under the [MIT Licence](LICENSE).

## Current template features

All ordinary workflows use authoring schema v3 and declare `authoring-schema-v3`.
Their cards highlight the information needed to identify or act on the workflow.
Document Review requires a document title and validated link. Delivery Tracking,
Purchase Approval and Event RSVP provide optional link actions that do not block
starting a workflow. Rejection and retry actions collect useful explanations.

Existing imports are independent definitions and are not updated automatically.
The app version must support v3 library entries before downloading these templates.
