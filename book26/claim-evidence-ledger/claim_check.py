"""Recompute what can be recomputed from the numbers printed in the paper. Nothing is invented.
Printed values carry 3 decimals, so each is uncertain by +/-0.0005; every check allows for that."""
import json, math
J=json.load(open("claims_input.json")); p=J["printed"]; TOL=0.0005
def within(computed_lo, computed_hi, printed): return computed_lo-1e-12<=printed<=computed_hi+1e-12
out=[]
KIND={"C1":"Arithmetic","C2":"Arithmetic","C3a":"Statistical","C3b":"Statistical","C4":"Statistical","C5":"Statistical","C6":"Clinical interpretation","C7":"Arithmetic"}
def rec(cid,statement,status,detail,agreement_by_construction=False):
    out.append(dict(id=cid,kind=KIND[cid],statement=statement,status=status,detail=detail,agreement_by_construction=agreement_by_construction))

# C1 radiologist average equals mean of the four printed individual F1s
ind=p["individual_radiologist_f1"]; lo=sum(x-TOL for x in ind)/4; hi=sum(x+TOL for x in ind)/4
ok=within(lo,hi,p["radiologist_avg_f1"]+0) or (lo-TOL<=p["radiologist_avg_f1"]<=hi+TOL)
rec("C1","The radiologist average F1 (0.387) is the mean of the four individual F1 values.",
    "Verified (arithmetic, from printed values)" if ok else "Contradicted",
    f"Mean of {ind} = {sum(ind)/4:.4f}; range allowing for rounding {lo:.4f} to {hi:.4f}; printed {p['radiologist_avg_f1']}. This shows the printed average is consistent with the arithmetic mean of the four printed scores. The text read describes it only as the average F1 across radiologists, so that it is defined as an arithmetic mean is an inference that fits the numbers, not a stated definition.")

# C2 difference of printed point estimates vs printed difference
d=p["chexnet_f1"]-p["radiologist_avg_f1"]; dlo=d-2*TOL; dhi=d+2*TOL
ok2=dlo<=p["difference"]<=dhi
rec("C2","The F1 difference (0.051) equals CheXNet F1 minus the radiologist average.",
    "Verified" if ok2 else "Partially supported: printed values do not reproduce it",
    f"0.435 - 0.387 = {d:.3f}; allowing for rounding of both inputs {dlo:.3f} to {dhi:.3f}; printed 0.051 lies {'inside' if ok2 else 'outside'} that range. The paper says the difference was computed on the same bootstrap samples, so the printed difference may be a different statistic (for example a mean of resampled differences). The text read does not say. This is an unexplained discrepancy, not a demonstrated error.")

# C3 CI midpoints (symmetry check)
for name,pt,ci in [("CheXNet",p["chexnet_f1"],p["chexnet_ci"]),("radiologist average",p["radiologist_avg_f1"],p["radiologist_avg_ci"])]:
    mid=(ci[0]+ci[1])/2
    rec("C3"+("a" if name=="CheXNet" else "b"),f"The {name} F1 interval is centred near the point estimate.",
        "Consistent (not a verification)",
        f"Midpoint {mid:.4f} vs point {pt}. Percentile-bootstrap intervals can be asymmetric, especially for a nonlinear statistic such as F1, so being centred near the estimate is neither required nor a check on the interval. This is a weak plausibility signal only and says nothing about whether the F1 itself is right.",True)

# C4 implied correlation between the two bootstrap F1 values
z=3.92
sa=(p["chexnet_ci"][1]-p["chexnet_ci"][0])/z; sb=(p["radiologist_avg_ci"][1]-p["radiologist_avg_ci"][0])/z
sd=(p["difference_ci"][1]-p["difference_ci"][0])/z
rho=(sa*sa+sb*sb-sd*sd)/(2*sa*sb)
rec("C4","The difference interval (0.005 to 0.084) is compatible with the two F1 intervals.",
    "Consistent (plausibility only; not independently checkable without the per-image data)",
    f"Normal-approximation standard errors: CheXNet {sa:.4f}, radiologists {sb:.4f}, difference {sd:.4f}. Treating the percentile intervals as if they were symmetric normal intervals, these imply a correlation of {rho:.2f} between the two resampled F1 values. That is an exploratory approximation, not a reconstruction or a check of the published bootstrap, and its only use is to see whether the three intervals could plausibly belong together when both F1 values are scored on the same 420 images.")

# C7 average vs every radiologist
best=max(ind); 
rec("C7","A reader might assume that exceeding the average radiologist means exceeding each radiologist.",
    "Contradicted by the printed values" if best>p["chexnet_f1"] else "Verified",
    f"The highest printed individual F1 is {best} (radiologist 4), above CheXNet's {p['chexnet_f1']}. Exceeding the average is not exceeding every radiologist. The text read gives no interval for individual radiologists, so whether radiologist 4 and CheXNet differ meaningfully is not checkable here. The abstract does not claim to exceed every radiologist; the check guards against a reader assuming it does.")
# C5 not checkable
rec("C5","CheXNet F1 = 0.435 (95% CI 0.387 to 0.481) on 420 images.","Not independently checkable",
    "Needs per-image predictions and labels, or at least the number of pneumonia-positive images, none of which is in the text read. The bootstrap (10,000 resamples) cannot be rerun. Recorded for the reader: the paper says the difference was computed on the same bootstrap samples (paired resampling). Whether unrounded values were used is not stated in the text read, and subtracting the displayed point estimates does not reproduce the whole analysis.")
# C6 logical connection
rec("C6","'CheXNet exceeds average radiologist performance on the F1 metric' (abstract).","Partially supported",
    "What the printed numbers support: a higher F1 on one 420-image set, with a difference interval whose lower bound (0.005) is close to zero. What they do not establish: performance in clinical use, performance on other hospitals' images, or that F1 against these labels measures diagnostic quality. The paper itself names frontal-only images and no patient history as limits. The abstract wording is about F1; a reader should not carry it over to 'radiologist-level pneumonia detection' without the qualifiers.")
out.sort(key=lambda r:r["id"])
json.dump(out,open("ledger.json","w"),indent=1)
print(json.dumps(out,indent=1))
