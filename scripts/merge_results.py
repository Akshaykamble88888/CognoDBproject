import json, glob, csv
from pathlib import Path

rows=[]
for fn in glob.glob("results/raw/*.json"):
    with open(fn) as f:
        d=json.load(f)
    for r in d["workloads"]:
        rows.append(r)
out=Path("results/results_matrix.csv")
with out.open("w", newline="") as f:
    w=csv.DictWriter(f, fieldnames=["database","workload","count","min_ms","p50_ms","p95_ms","avg_ms","max_ms"])
    w.writeheader(); w.writerows(rows)
print(out)
