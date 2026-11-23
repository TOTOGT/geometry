"""Data-quality audit and weekly coordinator summary for the synthetic file.
Reads only synthetic_participants.csv. Every number in the report is computed here."""
import csv, json, datetime as dt, collections
ASOF=dt.date(2026,11,2); OVERDUE_DAYS=90
REQUIRED=["consent_date","consent_version","enrollment_date","baseline_visit_date"]
def d(s): return dt.date.fromisoformat(s) if s else None
rows=list(csv.DictReader(open("synthetic_participants.csv")))
flags=[]  # (study_id, rule, detail)
ids=collections.Counter(r["study_id"] for r in rows)
for sid,n in ids.items():
    if n>1: flags.append((sid,"duplicate_id",f"{n} rows share this study_id"))
for r in rows:
    sid=r["study_id"]
    for f in REQUIRED:
        if not r[f]: flags.append((sid,"missing_field",f"{f} is blank"))
    c,e,b,v2,v3=[d(r[k]) for k in ("consent_date","enrollment_date","baseline_visit_date","visit2_date","visit3_date")]
    if c and e and e<c: flags.append((sid,"sequence","enrollment before consent"))
    if c and b and b<c: flags.append((sid,"sequence","baseline visit before consent"))
    if b and v2 and v2<b: flags.append((sid,"sequence","visit 2 before baseline"))
    if v2 and v3 and v3<v2: flags.append((sid,"sequence","visit 3 before visit 2"))
    lc=d(r["last_contact_date"])
    if r["followup_status"]=="Active" and lc and (ASOF-lc).days>OVERDUE_DAYS:
        flags.append((sid,"overdue",f"last contact {(ASOF-lc).days} days before {ASOF}"))
    if r["followup_status"]=="Completed" and not r["visit3_date"]:
        flags.append((sid,"completed_missing_visit3","status Completed but visit 3 is blank"))
unique_ids=sorted(set(ids))
flagged=sorted({f[0] for f in flags})
by_rule=collections.Counter(f[1] for f in flags)
recs_by_rule={k:sorted({f[0] for f in flags if f[1]==k}) for k in by_rule}
open_q=sorted({r["study_id"] for r in rows if r["open_query"]=="Y"})
status=collections.Counter(r["followup_status"] for r in {r["study_id"]:r for r in rows}.values())
res=dict(asof=str(ASOF),rows=len(rows),participants=len(unique_ids),flagged_records=len(flagged),
  clean_records=len(unique_ids)-len(flagged),flags_total=len(flags),by_rule=dict(by_rule),
  records_by_rule=recs_by_rule,open_queries=len(open_q),status=dict(status),
  multi_flag=sorted(s for s in flagged if sum(1 for f in flags if f[0]==s)>1))
json.dump(res,open("audit_results.json","w"),indent=1)
with open("audit_flags.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["study_id","rule","detail"]); w.writerows(sorted(flags))
L=[f"# Weekly coordinator report (synthetic data), as of {ASOF}","",
 f"Participants (unique study IDs): {res['participants']}  |  rows in file: {res['rows']}",
 f"Status: "+", ".join(f"{k} {v}" for k,v in sorted(status.items())),
 f"Records with at least one flag: {res['flagged_records']}; with none: {res['clean_records']}",
 f"Total flags: {res['flags_total']} (a record can carry more than one flag)",
 f"Open data queries: {res['open_queries']}","","## Flags by rule (records)"]
for k,v in sorted(recs_by_rule.items()): L.append(f"- {k}: {len(v)} ({', '.join(v)})")
L+=["","## Records carrying more than one flag",", ".join(res["multi_flag"]) or "none","",
 "## What needs a person, not a script",
 "- Any consent question, a missing or inconsistent consent date or version: study-team lead and, where required, IRB.",
 "- Any apparent protocol deviation: PI.",
 "- Any clinical or safety question: clinical team. The coordinator does not decide these.",
 "- Duplicate IDs: resolve against source documents under the study's procedures; do not overwrite."]
open("weekly_report.md","w").write("\n".join(L)+"\n")
print(json.dumps(res,indent=1))
