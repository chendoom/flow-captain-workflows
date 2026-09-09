# Pinned authoring schemas

These immutable schema files are copied unchanged from chendoom-site commit
`3054bef02156a318f878e5d7825bc3ce36b05438`, `public/artifacts/v{version}/`.
They are the same contracts used by the app importer. Keeping a copy here makes
CI independent of website availability and deployment timing. Never widen an
existing version; add a new version and update the importer and catalogue together.

The canonical v3 website URL returned 404 when checked on 9 September 2026; its
site source is ready but requires a separate website deployment. Local and CI
validation use these pinned contracts in the meantime.

Workflow documents reference the local copy with a relative `$schema` path, so
editor validation works from a checkout without contacting the website. The app
selects its own strict decoder from `schemaVersion`, never from `$schema`.
