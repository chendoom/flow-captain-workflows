# Workflow Plans

Plans connect ordinary workflows while keeping each workflow useful on its
own. They describe ordering, role mappings, and typed data passed between
completed workflows.

[`group-trip.json`](group-trip.json) mirrors Flow Captain's built-in Group Trip
Plan. It deliberately keeps travellers separate from app roles: a traveller
does not need an account, and an authorised actor can enter a booking or
expense on their behalf.

Plan download and editing in the app is being introduced after the engine and
local replay support. Until that UI is available, these documents are the
public, reviewable source for the Plan shape and can be adapted through a pull
request without changing the built-in copy.
