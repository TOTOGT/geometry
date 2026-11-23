"""Control that can fail: compare the audit's flags with the defects the generator injected.
The audit never reads injected_defects.json."""
import json, csv
inj=json.load(open("injected_defects.json")); res=json.load(open("audit_results.json"))
flags=list(csv.DictReader(open("audit_flags.csv")))
ok=True
for rule,ids in inj.items():
    found={f["study_id"] for f in flags if f["rule"]==rule}
    missed=set(ids)-found; extra=found-set(ids)
    print(f"{rule}: injected {len(ids)}, found {len(found)}, missed {sorted(missed)}, unexpected {sorted(extra)}")
    ok&=not missed and not extra
print("PASS" if ok else "FAIL"); raise SystemExit(0 if ok else 1)
