"""Generate a fully synthetic participant-tracking file. Every record is fictional.
Seeded, so the output is identical on every run. Writes the CSV plus a separate
injected_defects.json that the audit script never reads (used only by verify.py)."""
import csv, json, random, datetime as dt
random.seed(2026)
D=dt.date
def iso(d): return d.isoformat() if d else ""
rows=[]; injected={"missing_field":[],"duplicate_id":[],"sequence":[],"overdue":[],"completed_missing_visit3":[]}
base=D(2026,1,12)
for i in range(1,31):
    sid=f"SYN-{i:03d}"
    consent=base+dt.timedelta(days=i*6+random.randint(0,3))
    enroll=consent+dt.timedelta(days=random.randint(1,4))
    b=enroll+dt.timedelta(days=random.randint(2,7))
    v2=b+dt.timedelta(days=random.randint(80,100))
    v3=v2+dt.timedelta(days=random.randint(80,100))
    status=random.choice(["Active"]*4+["Completed","Withdrawn"])
    r=dict(study_id=sid,site=random.choice("AB"),age_group=random.choice(["0-4","5-9","10-14","15-18"]),
      consent_date=consent,consent_version="v2",enrollment_date=enroll,baseline_visit_date=b,
      visit2_date=v2,visit3_date=v3,last_contact_date=None,followup_status=status,open_query=random.choice(["N"]*4+["Y"]))
    asof=D(2026,11,2)
    # visits that have not happened yet by the as-of date are blank, not errors
    for k in ("visit2_date","visit3_date"):
        if r[k]>asof: r[k]=None
    last=max([x for x in (r["baseline_visit_date"],r["visit2_date"],r["visit3_date"]) if x])
    r["last_contact_date"]=min(last+dt.timedelta(days=random.randint(0,20)),asof)
    if status=="Completed": r["visit3_date"]=r["visit3_date"] or last+dt.timedelta(days=5)
    rows.append(r)
by={r["study_id"]:r for r in rows}
# inject known defects
for sid,field in [("SYN-004","consent_date"),("SYN-011","baseline_visit_date"),("SYN-017","consent_version"),("SYN-023","enrollment_date")]:
    by[sid][field]=None; injected["missing_field"].append(sid)
by["SYN-008"]["enrollment_date"]=by["SYN-008"]["consent_date"]-dt.timedelta(days=3); injected["sequence"].append("SYN-008")
by["SYN-014"]["visit2_date"]=by["SYN-014"]["baseline_visit_date"]-dt.timedelta(days=10); injected["sequence"].append("SYN-014")
by["SYN-026"]["baseline_visit_date"]=by["SYN-026"]["consent_date"]-dt.timedelta(days=1); injected["sequence"].append("SYN-026")
for sid in ["SYN-002","SYN-011","SYN-020"]:
    by[sid]["followup_status"]="Active"; by[sid]["last_contact_date"]=D(2026,6,20); injected["overdue"].append(sid)
for sid in ["SYN-006","SYN-021"]:
    by[sid]["followup_status"]="Completed"; by[sid]["visit3_date"]=None; injected["completed_missing_visit3"].append(sid)
dup=dict(by["SYN-009"]); dup["site"]="B" if dup["site"]=="A" else "A"; rows.append(dup); injected["duplicate_id"].append("SYN-009")
cols=list(rows[0].keys())
with open("synthetic_participants.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({k:iso(v) if isinstance(v,dt.date) else (v or "") for k,v in r.items()})
json.dump(injected,open("injected_defects.json","w"),indent=1)
print("rows",len(rows))
