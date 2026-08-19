#!/usr/bin/env python3
"""
claims.py — audit what the corpus ASSERTS, not how it is built.

tools/audit.py checks structure: tags balance, links resolve, files close.
It certified book4 clean while book4/ch11-catgt.html attributed Vol I's DOI
to CatGT. A correctly-formed DOI pointing at the wrong work is invisible to a
structural auditor and fatal to a reader who clicks it. This tool covers that
gap. Every rule below carries the reason it exists.

Rules
-----
DOI-TITLE   A DOI is quoted next to a work title. Resolve the DOI against
            Zenodo and compare. Origin: gomc-opus.html, book4/gomc-opus.html
            and book4/ch11-catgt.html all cite 10.5281/zenodo.19117399 as
            CatGT. That record is "Principia Orthogona, Volume I".

DOI-ALIAS   A DOI appears in a context naming a different work than the one it
            resolves to, even without a quoted title. Catches the same defect
            in prose and in footers, where the title is not quoted.

WITHDRAWN   A claim that was retracted or corrected but survives in some copies.
            Origin: "Raiz da série" / "Series DOI" — the series-root claim was
            withdrawn, and it is still live in 20 files. Also the seventeen-file
            "Submetido ao IMPA" cleanup, which missed book4/ch10.

PENDING     A submission/status claim that was true when written and decays
            silently: "Submitted to X", "In review", "Forthcoming". These
            cannot be machine-verified — the tool lists them with the file's
            last-modified date so they can be re-confirmed on a schedule.
            Origin: "Submitted to Catalysis Today", a journal that accepts no
            unsolicited submissions at all.

FORECAST    A projection stated as fact. Origin: "will collide in 4.5 billion
            years", where the source says "projected". Still live in
            book8/ch8-3-galaxy-mergers.html after the d3cb60e fix hit a
            different copy.

ISBN        An ISBN not in the canonical registry. Origin: unallocated 5-6
            reserve printed in two Book 8 footers.

CONFLICT    Merge artifacts committed as content: *-REMOTE.html, *-LOCAL.html,
            *-BACKUP.html, or conflict markers in the body. Origin: thirteen
            _archive/book7/*-REMOTE.html files, which are reachable link
            targets, not archives.

Suppressions live in SUPPRESS below, in the tool, with a reason — never in
someone's memory of which warnings are fine.

Usage
-----
    python3 tools/claims.py                 # whole tree
    python3 tools/claims.py book4 index.html
    python3 tools/claims.py --offline       # skip Zenodo, use cache only
    python3 tools/claims.py --json report.json
"""

import argparse
import datetime as _dt
import html as _html
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".doi-cache.json")
SKIP_DIRS = {".git", "node_modules", "_to_delete", ".venv", "__pycache__"}

# ---------------------------------------------------------------- known works
# Aliases used in prose for each Zenodo record. Populated from the corpus's own
# vocabulary. A DOI whose context names an alias belonging to a DIFFERENT record
# is a misattribution.
ALIASES = {
    "19117399": [
        "principia orthogona", "volume i", "vol. i", "vol i",
        "mathematics of generative transitions",
    ],
    "21296707": [
        "operator firing order", "ethanol-to-hydrocarbon", "ethanol to hydrocarbon",
    ],
}
# Aliases that must NOT appear next to a DOI unless that DOI is theirs.
FOREIGN_ALIASES = {
    "catgt": "Catalytic Generative Theory",
    "catalytic generative theory": "Catalytic Generative Theory",
    "generative temporal contact": "Generative Temporal Contact Theory",
    "gtct": "Generative Temporal Contact Theory",
}

# ------------------------------------------------------------- literal rules
WITHDRAWN = [
    (r"Ra[ií]z da s[ée]rie", "series-root claim was withdrawn"),
    (r"S[ée]rie[s]?\s+DOI", "'Series DOI' mislabels a volume DOI as the series root"),
    (r"Submetido ao IMPA", "IMPA declined; label cleared in ce0134c"),
    (r"Submitted to IMPA", "IMPA declined; label cleared in ce0134c"),
]

PENDING = [
    (r"Submitted to ([A-Z][\w &.\-']{2,60})", "submission status decays silently"),
    (r"Submetido a[o]? ([A-Z][\w &.\-']{2,60})", "submission status decays silently"),
    (r"\b(In review|Under review|Forthcoming|In press)\b", "status decays silently"),
]

FORECAST = [
    (r"will collide in [\d.]+ billion years",
     "projection stated as fact; van der Marel says 'projected'"),
    (r"\bwill (?:be published|appear) in\b", "unscheduled future stated as fact"),
]

CONFLICT_NAMES = re.compile(r"-(REMOTE|LOCAL|BACKUP|BASE)\.html$", re.I)
CONFLICT_MARKERS = re.compile(r"^(<{7} |={7}$|>{7} )", re.M)

# ISBNs known to be allocated. Anything else printed as an ISBN is flagged.
# Empty list = flag every ISBN found, which is the safe default until the
# canonical registry is pointed at with --isbn-registry.
ISBN_REGISTRY = set()

SUPPRESS = [
    # (rule, path-substring, reason)
    ("PENDING", "on-publication.html",
     "that page's subject IS submission status; entries are reviewed there"),
    ("DOI-TITLE", "/tools/",
     "tooling and fixtures quote DOIs as examples, not as claims"),
]

DOI_RE = re.compile(r"10\.5281/zenodo\.(\d{6,9})")
QUOTED_TITLE_RE = re.compile(r'["“‘]([^"”’]{4,140})["”’]')
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
STOP = {
    "the", "a", "an", "of", "and", "in", "on", "for", "to", "vol", "volume",
    "part", "version", "zenodo", "doi", "grossi", "p.n.", "pn", "llc", "g6",
}


def text_of(chunk):
    return WS_RE.sub(" ", _html.unescape(TAG_RE.sub(" ", chunk))).strip()


SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.I | re.S)
ANY_TAG_RE = re.compile(r"<[^>]*>", re.S)


def mask(src):
    """Blank every tag and every script/style body with spaces, preserving
    length so offsets into the mask are offsets into the source.

    Why this exists: the first version of DOI-TITLE sliced context straight out
    of the raw source and ran a quoted-string regex over it. Slicing mid-tag
    leaves attribute fragments behind, so it reported things like
    ``cites " target=" as 20710023`` and ``cites "_blank" as ...`` — 200-odd
    findings that were all the same bug in this tool. Masking first means the
    context a rule sees is what a reader sees.
    """
    buf = list(src)
    for rx in (SCRIPT_STYLE_RE, ANY_TAG_RE):
        for m in rx.finditer("".join(buf)):
            for i in range(m.start(), m.end()):
                if buf[i] != "\n":
                    buf[i] = " "
    return "".join(buf)


# A quoted run only counts as a claimed title if it reads like prose: at least
# two words, no markup/CSS/JS punctuation, not a bare identifier.
BAD_TITLE_CHARS = set("=<>{};#|\\")


def looks_like_title(s):
    s = s.strip()
    if len(s) < 8 or len(s.split()) < 2:
        return False
    if BAD_TITLE_CHARS & set(s):
        return False
    if not re.search(r"[A-Za-z]{3}", s):
        return False
    return True


def tokens(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}


# ------------------------------------------------------------------- Zenodo
def load_cache():
    try:
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def save_cache(c):
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(c, fh, indent=1, sort_keys=True)


def resolve(rec_id, cache, offline):
    """Return the Zenodo record title for a record id, or None."""
    if rec_id in cache:
        return cache[rec_id]
    if offline:
        return None
    url = "https://zenodo.org/api/records/%s" % rec_id
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            title = json.load(r)["metadata"]["title"]
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError) as e:
        title = {"__error__": "%s: %s" % (type(e).__name__, e)}
    cache[rec_id] = title
    return title


# ------------------------------------------------------------------- engine
# A repo that documents its own defects contains correct prose matching every
# defect pattern. CLAUDE.md records this trap three separate times — the
# master-index anchor-label sweep, the 19117399 relabel sweep (which nearly
# rewrote HVEH/proofs/index.html's *denial* "no single series DOI" into its
# opposite), and audit.py, which was flagging CLAUDE.md's own corrections.
# Any rule that matches a claim must therefore ask whether the match sits
# inside a notice retracting that claim.
CORRECTION_MARKERS = [
    "correction", "corrected", "corrigid", "correcao", "correção",
    "withdrawn", "withdrew", "retired", "retracted", "superseded",
    "unallocated", "reserva", "não alocad", "nao alocad",
    "no single series", "is not a series", "not a series doi",
    "there is no series", "mislabel", "phantom", "do not restore",
    "stale", "this claim was", "no longer", "errata",
]


def in_correction_context(masked, pos, span=700):
    """True if the match sits inside prose that is retracting the claim."""
    window = masked[max(0, pos - span): pos + span].lower()
    return any(mk in window for mk in CORRECTION_MARKERS)


def suppressed(rule, path):
    for r, frag, _why in SUPPRESS:
        if r == rule and frag in path.replace(os.sep, "/"):
            return True
    return False


def line_of(src, pos):
    return src.count("\n", 0, pos) + 1


def walk(targets):
    for t in targets:
        if os.path.isfile(t):
            yield t
            continue
        for dirpath, dirnames, filenames in os.walk(t):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in sorted(filenames):
                if fn.endswith(".html"):
                    yield os.path.join(dirpath, fn)


def scan(path, src, cache, offline, findings):
    rel = os.path.relpath(path, ROOT)
    masked = mask(src)

    def add(rule, line, msg, why, pos=None):
        if pos is not None and in_correction_context(masked, pos):
            return
        if not suppressed(rule, rel):
            findings.append({"rule": rule, "file": rel, "line": line,
                             "message": msg, "why": why})

    # --- CONFLICT
    if CONFLICT_NAMES.search(os.path.basename(path)):
        add("CONFLICT", 1, "merge-artifact filename committed as content",
            "*-REMOTE/LOCAL/BACKUP are conflict copies, and they are reachable")
    m = CONFLICT_MARKERS.search(src)
    if m:
        add("CONFLICT", line_of(src, m.start()), "unresolved conflict marker in body",
            "a conflict marker in shipped HTML renders as literal text")

    # --- literal rules
    for pattern, why in WITHDRAWN:
        for m in re.finditer(pattern, src, re.I):
            add("WITHDRAWN", line_of(src, m.start()), m.group(0).strip(), why,
                pos=m.start())
    for pattern, why in FORECAST:
        for m in re.finditer(pattern, src, re.I):
            add("FORECAST", line_of(src, m.start()), m.group(0).strip(), why,
                pos=m.start())
    for pattern, why in PENDING:
        for m in re.finditer(pattern, src):
            mtime = _dt.date.fromtimestamp(os.path.getmtime(path)).isoformat()
            add("PENDING", line_of(src, m.start()),
                "%s  (file last touched %s)" % (m.group(0).strip(), mtime), why)

    # --- ISBN
    for m in re.finditer(r"ISBN[^0-9]{0,12}((?:97[89][- ]?)?[\d][\d\- ]{8,15}[\dXx])", src):
        raw = re.sub(r"[^0-9Xx]", "", m.group(1))
        if ISBN_REGISTRY and raw not in ISBN_REGISTRY:
            add("ISBN", line_of(src, m.start()), "ISBN %s not in registry" % raw,
                "unallocated ISBNs were printed in two Book 8 footers")
        elif not ISBN_REGISTRY:
            add("ISBN", line_of(src, m.start()),
                "ISBN %s (no registry loaded — pass --isbn-registry to check)" % raw,
                "unallocated ISBNs were printed in two Book 8 footers",
                pos=m.start())

    # --- DOI rules
    for m in DOI_RE.finditer(src):
        rec = m.group(1)
        line = line_of(src, m.start())
        # Context comes from the masked document, never the raw source — see
        # mask() for the false-positive class this prevents.
        ctx = text_of(masked[max(0, m.start() - 340): m.end() + 180])
        low = ctx.lower()

        title = resolve(rec, cache, offline)
        if isinstance(title, dict):
            add("DOI-DEAD", line, "%s did not resolve (%s)" % (rec, title["__error__"]),
                "a DOI that does not resolve is a dead citation, and unlike a "
                "title mismatch this needs no judgement to confirm")
            continue
        if title is None:
            continue

        # DOI-ALIAS: context names a work this record is not.
        own = ALIASES.get(rec, [])
        tl = title.lower()
        for alias, workname in FOREIGN_ALIASES.items():
            # If the record's OWN title contains the alias, the citation is
            # correct and there is nothing to flag. Why this guard exists:
            # "GTCT" expands to "Generative Time Circuit Theorem" in several
            # Zenodo titles and to "Generative Temporal Contact Theory" in the
            # prose. Without this check the rule reported 14 correct citations
            # as misattributions — the acronym collision is a real editorial
            # problem, but it is not a wrong DOI.
            if alias in tl or workname.lower() in tl:
                continue
            if alias in low and not any(a in low for a in own):
                add("DOI-ALIAS", line,
                    "%s cited near \"%s\" but resolves to \"%s\"" % (rec, workname, title),
                    "a correctly-formed DOI on the wrong work is invisible to a "
                    "structural audit and fatal to a reader who clicks it",
                    pos=m.start())
                break

        # DOI-TITLE: an explicitly quoted title adjacent to the DOI.
        doi_at = ctx.lower().find("zenodo." + rec)
        near = []
        for q in QUOTED_TITLE_RE.finditer(ctx):
            if not looks_like_title(q.group(1)):
                continue
            gap = doi_at - q.end() if doi_at >= 0 else 10 ** 6
            if 0 <= gap <= 90:
                near.append((gap, q.group(1)))
        if near:
            claimed = min(near)[1]
            ct, rt = tokens(claimed), tokens(title)
            if ct and rt and not (ct & rt):
                add("DOI-TITLE", line,
                    "cites \"%s\" as %s, which is \"%s\"" % (claimed, rec, title),
                    "quoted title shares no significant word with the Zenodo record",
                    pos=m.start())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="*", default=[ROOT])
    ap.add_argument("--offline", action="store_true", help="use the DOI cache only")
    ap.add_argument("--json", metavar="PATH", help="also write findings as JSON")
    ap.add_argument("--isbn-registry", metavar="PATH",
                    help="file of allocated ISBNs, one per line")
    ap.add_argument("--rule", action="append",
                    help="only report these rules (repeatable)")
    args = ap.parse_args()

    if args.isbn_registry:
        with open(args.isbn_registry, encoding="utf-8") as fh:
            for ln in fh:
                v = re.sub(r"[^0-9Xx]", "", ln)
                if v:
                    ISBN_REGISTRY.add(v)

    targets = args.targets or [ROOT]
    cache, findings, n = load_cache(), [], 0
    for path in walk(targets):
        n += 1
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                src = fh.read()
        except OSError as e:
            print("  ! unreadable %s (%s)" % (path, e), file=sys.stderr)
            continue
        scan(path, src, cache, args.offline, findings)
    save_cache(cache)

    seen, uniq = set(), []
    for f in findings:
        k = (f["rule"], f["file"], f["line"], f["message"])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    findings = uniq

    if args.rule:
        keep = {r.upper() for r in args.rule}
        findings = [f for f in findings if f["rule"] in keep]

    order = ["DOI-ALIAS", "DOI-DEAD", "WITHDRAWN", "CONFLICT", "DOI-TITLE",
             "FORECAST", "ISBN", "PENDING"]
    findings.sort(key=lambda f: (order.index(f["rule"]) if f["rule"] in order else 99,
                                 f["file"], f["line"]))

    print("%d html scanned in: %s" % (n, ", ".join(os.path.relpath(t, ROOT)
                                                   for t in targets)))
    if not findings:
        print("  clean")
    cur = None
    for f in findings:
        if f["rule"] != cur:
            cur = f["rule"]
            print("\n== %s — %s" % (cur, f["why"]))
        print("  %s:%d  %s" % (f["file"], f["line"], f["message"]))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(findings, fh, indent=1)
        print("\nwrote %s" % args.json)

    # Only rules that need no judgement gate the exit code. DOI-TITLE, ISBN,
    # FORECAST and PENDING are review queues: a human confirms them.
    hard = [f for f in findings if f["rule"] in
            ("DOI-ALIAS", "DOI-DEAD", "WITHDRAWN", "CONFLICT")]
    print("\n%d finding(s); %d require a fix, %d require a human decision"
          % (len(findings), len(hard), len(findings) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
