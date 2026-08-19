import csv, json, random, time
from pathlib import Path
from .config import DATABASES
from .neo4j_adapter import CypherAdapter
from .queries import INSERT_BATCH, Q_1HOP, Q_2HOP, Q_3HOP, Q_POINT, Q_FILTER, Q_AGG, CREATE_INDEX
from .stats import summarize

WARMUP = 20
ITERATIONS = 100
BATCH_SIZE = 500

def load_edges(path, limit=100_000):
    edges = []
    nodes = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src, dst = int(row["src"]), int(row["dst"])
            edges.append((src, dst))
            nodes.update((src, dst))
            if len(edges) >= limit:
                break
    return edges, sorted(nodes)

def run_cypher(name, cfg, edges, nodes):
    adapter = CypherAdapter(cfg["uri"], cfg["user"], cfg["password"])
    try:
        adapter.run("MATCH (n) DETACH DELETE n")
        t0 = time.perf_counter()
        for i in range(0, len(edges), BATCH_SIZE):
            rows = [{"src": s, "dst": d} for s, d in edges[i:i+BATCH_SIZE]]
            adapter.write_batch(INSERT_BATCH, rows)
        load_s = time.perf_counter() - t0
        adapter.run(CREATE_INDEX)

        sample = random.Random(42).sample(nodes, min(100, len(nodes)))
        workloads = {
            "1hop": Q_1HOP,
            "2hop": Q_2HOP,
            "3hop": Q_3HOP,
            "point_lookup": Q_POINT,
            "filtered_lookup": Q_FILTER,
            "aggregation": Q_AGG,
        }
        results = []
        for workload, query in workloads.items():
            for _ in range(WARMUP):
                if workload == "filtered_lookup":
                    adapter.run(query, lo=sample[0], hi=sample[0]+1000)
                elif workload == "aggregation":
                    adapter.run(query)
                else:
                    adapter.run(query, id=random.choice(sample))
            times = []
            for _ in range(ITERATIONS):
                if workload == "filtered_lookup":
                    lo = random.choice(sample)
                    t = adapter.timed(query, lo=lo, hi=lo+1000)
                elif workload == "aggregation":
                    t = adapter.timed(query)
                else:
                    t = adapter.timed(query, id=random.choice(sample))
                times.append(t)
            s = summarize(times)
            s.update(database=name, workload=workload)
            results.append(s)

        out = Path("results/raw")
        out.mkdir(parents=True, exist_ok=True)
        with open(out / f"{name}.json", "w") as f:
            json.dump({"load_seconds": load_s, "nodes": len(nodes), "relationships": len(edges), "workloads": results}, f, indent=2)
        print(name, "load_seconds=", round(load_s, 3))
    finally:
        adapter.close()

if __name__ == "__main__":
    edges, nodes = load_edges("data/pokec_edges.csv", limit=100_000)
    for name in ["cognodb", "neo4j", "memgraph"]:
        cfg = DATABASES[name]
        if cfg["uri"] and cfg["password"] is not None:
            run_cypher(name, cfg, edges, nodes)
        else:
            print("Skipping", name, "- credentials missing")
