# CognoDB Cloud Benchmark — Assignment 1

This repository benchmarks CognoDB Cloud against comparable graph databases using the same dataset and logical workloads.

## Assignment alignment

The Wexa AI assignment asks for:
- CognoDB plus at least four other graph databases
- a public dataset with at least 100,000 relationships
- identical data and logical workloads
- warm-up and repeated measurements
- p50 and p95 latency
- ingest throughput
- point/indexed lookup
- aggregation
- concurrent mixed read/write workload
- resource/footprint reporting
- reproducible automation and honest caveats

See the assignment requirements in the supplied brief. fileciteturn0file0L34-L43

## Important methodology note

Do NOT claim that the benchmark is fair until the instance CPU/RAM/storage and region have been recorded for every database. The assignment explicitly requires equivalent resources and the same client machine/region. fileciteturn0file0L74-L79

## Candidate databases

Initial harness:
1. CognoDB Cloud
2. Neo4j AuraDB
3. Memgraph
4. FalkorDB
5. ArangoDB

If a platform cannot provide an equivalent resource tier, use a self-hosted deployment capped to the agreed CPU/RAM/storage and document that decision.

## Dataset

The preparation script samples the first 100,000 relationships from SNAP soc-Pokec. The original SNAP dataset is much larger; this repository intentionally samples a small reproducible slice so it can fit constrained instances. Source: https://snap.stanford.edu/data/soc-Pokec.html

Run:

```bash
python scripts/prepare_pokec.py
```

## Local setup

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` with credentials. Never commit it.

## Run

```bash
python scripts/prepare_pokec.py
python -m benchmark.runner
python scripts/merge_results.py
```

The current starter runner executes the Cypher-compatible subset (CognoDB, Neo4j, Memgraph). FalkorDB and ArangoDB require their adapter implementations before they are included in final results.

## Final benchmark requirements still to implement

1. FalkorDB adapter
2. ArangoDB AQL adapter
3. concurrent mixed read/write test at 1/10/40 clients
4. ingest nodes/sec and relationships/sec
5. resource/footprint collection
6. cold-start run, if reported
7. result charts
8. final README results matrix and caveats

## Security

Passwords and connection URIs must come from environment variables. Never put secrets in GitHub. The assignment explicitly prohibits committing passwords or connection URIs. fileciteturn0file0L122-L128
