# Workflow Plans

Group Trip now has two phases: **Trip Proposal → Trip Expenses**. People suggest
destinations, the organiser chooses a most-suggested destination (including any
tied winner), and the chosen destination and participant records pass into expense
tracking. The trip name is prominent; the organiser can maintain optional booking
links while expenses are being recorded.

[`group-trip.json`](group-trip.json) is the library review manifest for the matching
bundled Group Trip Plan, version 11. Its child references pin Trip Proposal 14 and
Trip Expenses 14. The app can review this library entry and open the included Plan.
It does not yet import arbitrary public Plan definitions or download child artifacts.
The start form and its complete typed inputs come from the pinned proposal child;
this manifest deliberately does not duplicate that participant-record schema.

Travellers are domain records and do not all need app accounts. Plan roles identify
people authorised to use the app; an organiser can act for a traveller without an
account. Contributor history retains the acting app member.

Plan review documents keep their separate schema version 1. The ordinary workflow
library uses authoring schema v3. New bundled Plan and child versions retain old
artifacts so existing journeys continue using their original versions.
