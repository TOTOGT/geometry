"""A check that can fail: alter printed numbers and confirm the arithmetic checks notice."""
import json, subprocess, shutil
J=json.load(open("claims_input.json"))
J["printed"]["radiologist_avg_f1"]=0.397; J["printed"]["difference"]=0.038
json.dump(J,open("claims_input_altered.json","w"))
src=open("claim_check.py").read().replace("claims_input.json","claims_input_altered.json").replace("ledger.json","ledger_altered.json")
open("_altered_check.py","w").write(src); subprocess.run(["python3","_altered_check.py"],capture_output=True)
L={r["id"]:r["status"] for r in json.load(open("ledger_altered.json"))}
print("C1 with altered average:",L["C1"]); print("C2 with altered difference:",L["C2"])
assert L["C1"].startswith("Contradicted"), "control failed: altered average not caught"
print("CONTROL PASS: the checks fail when the printed numbers are wrong")
