# _archive/MANIFEST.md — geometry repo cleanup, 2026-07-12

Prompted by: "too many portals and hubs with no apparent use." Audited every
`*hub*.html` / `*portal*.html` / `*gateway*.html` / `*labyrinth*.html` /
`*access*.html` file plus every `-REMOTE`/`-LOCAL`/`-BASE`/`copy`-named file
for actual incoming links (`grep -rl <basename> --include="*.html" .`).
Nothing was deleted — moved here, paths preserved, per the house rule in
`~/Desktop/dnls/CLAUDE.md` ("never delete... move stale files to
`<folder>/_archive/` and write a MANIFEST.md").

**Files kept live (heavily referenced, real navigation infrastructure —
not touched):** `series-hub.html` (244 refs), `hub.html` (260 refs),
`portal.html` (124 refs), `Sportal.html` (42 refs), `book4/hub.html`
(261 refs), `impa-portal.html` (113 refs), `chEta-tribonacci.html`
(25 refs), `labyrinth.html`. These are the actual site skeleton — the
"too many" complaint is about the files below, not these.

---

## Group 1 — git-merge `-REMOTE.html` artifacts (22 files, 0 references each)

These are leftover 3-way-merge-tool byproducts (the `-REMOTE` suffix is a
standard git mergetool naming convention for "their" version during an
unresolved/uncleaned conflict). Every one of them has zero incoming
`<a href>` references anywhere in the repo, and 21 of the 22 have a
same-named non-`-REMOTE` sibling that IS live and linked — confirming
these are debris from past merges (some likely from this session's own
book7/ch-noether.html + book7/ch-turing.html conflict resolution, or
earlier ones), not distinct content anyone points to.

| Archived file | Live sibling (unaffected) |
|---|---|
| `book7/ch-bak-REMOTE.html` | `book7/ch-bak.html` |
| `book7/ch-dyson-REMOTE.html` | `book7/ch-dyson.html` |
| `book7/ch-hopfield-REMOTE.html` | `book7/ch-hopfield.html` |
| `book7/ch-katherine-johnson-REMOTE.html` | `book7/ch-katherine-johnson.html` |
| `book7/ch-klein-thymus-REMOTE.html` | `book7/ch-klein-thymus.html` |
| `book7/ch-kovalevskaya-REMOTE.html` | `book7/ch-kovalevskaya.html` |
| `book7/ch-mirzakhani-REMOTE.html` | `book7/ch-mirzakhani.html` |
| `book7/ch-mitchison-kirschner-REMOTE.html` | `book7/ch-mitchison-kirschner.html` |
| `book7/ch-noether-REMOTE.html` | `book7/ch-noether.html` |
| `book7/ch-thom-REMOTE.html` | `book7/ch-thom.html` |
| `book7/ch-turing-REMOTE.html` | `book7/ch-turing.html` |
| `book7/ch-victora-nussenzweig-REMOTE.html` | `book7/ch-victora-nussenzweig.html` |
| `book7/ch-waddington-REMOTE.html` | `book7/ch-waddington.html` |
| `omega/ch-rumi-REMOTE.html` | `omega/ch-rumi.html` |
| `book6/index-REMOTE.html` | `book6/index.html` |
| `chDis-disaster-REMOTE.html` | `chDis-disaster.html` |
| `chE-gtct-REMOTE.html` | `chE-gtct.html` |
| `chEps-gronwall-REMOTE.html` | `chEps-gronwall.html` |
| `chEta-tribonacci-REMOTE.html` | `chEta-tribonacci.html` |
| `chMu-lyapunov-REMOTE.html` | `chMu-lyapunov.html` |
| `chOmega-hexabonacci-REMOTE.html` | `chOmega-hexabonacci.html` |
| `vol1-mathematics-REMOTE.html` | `vol1-mathematics.html` (content differs more than the others — worth a quick diff if you ever want the REMOTE version back, but it's still 0-referenced) |

## Group 2 — files CLAUDE.md itself already flagged as archive candidates

From `~/Desktop/dnls/CLAUDE.md`'s "known issues queued for future sessions"
(§5): *"Files that may belong in `_archive/` rather than the live map:
`access-required_copy`, `journey-v1-backup`, `course-16weeks-source`,
`impa-portal-patch`."* Confirmed via link-check before moving:

| Archived file | Who referenced it | Note |
|---|---|---|
| `access-required_copy.html` | `livro3-brasil.html` | Finder-duplicate name; `access-required.html` is the real page |
| `journey-v1-backup.html` | `chapters-diagram.html` | Explicit backup filename |
| `course-16weeks-source.html` | `chapters-diagram.html` | Explicit "-source" backup filename |
| `impa-portal-patch.html` | `chapters-diagram.html` | A 3,991-byte patch fragment, same size as its target — reads like an unmerged diff, not a standalone page |
| `index-geometry-hub.html` | `chapters-diagram.html` | — |

**Known consequence:** `chapters-diagram.html` now has 5 dead links (plus
whatever the `-REMOTE` files broke, if anything did — checked, none of
those had inbound links from it). This is not a new problem: `CLAUDE.md`
already documents `chapters-diagram.html` as stale and queued for a full
rebuild against the real 112+-file roster. This cleanup doesn't fix that
page; it just stops pretending these 5 files are live content elsewhere.

---

## What this does NOT resolve

The heavily-linked hub files (`hub.html`, `portal.html`, `series-hub.html`,
`book4/hub.html`, `Sportal.html`) still overlap in purpose and were not
touched — consolidating *those* is a bigger content decision (which one is
the "real" entry point, whether the others become redirects) that needs a
call, not a link-count. Flagging for a future pass if still wanted.
