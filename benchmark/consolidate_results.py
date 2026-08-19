import json
import os
import csv


RESULTS_DIR = "results"
OUTPUT_FILE = "results/cognodb_summary.csv"


def load_json(filename):

    path = os.path.join(
        RESULTS_DIR,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    traversal = load_json(
        "cognodb_traversal_random.json"
    )

    lookup = load_json(
        "cognodb_lookup.json"
    )

    aggregation = load_json(
        "cognodb_aggregation.json"
    )

    mixed = load_json(
        "cognodb_mixed_workload.json"
    )

    rows = [

        {
            "category": "Traversal",
            "metric": "1-hop",
            "p50_ms": traversal["1-hop"]["p50_ms"],
            "p95_ms": traversal["1-hop"]["p95_ms"]
        },

        {
            "category": "Traversal",
            "metric": "2-hop",
            "p50_ms": traversal["2-hop"]["p50_ms"],
            "p95_ms": traversal["2-hop"]["p95_ms"]
        },

        {
            "category": "Traversal",
            "metric": "3-hop",
            "p50_ms": traversal["3-hop"]["p50_ms"],
            "p95_ms": traversal["3-hop"]["p95_ms"]
        },  

        {
            "category": "Lookup",
            "metric": "Point lookup",
            "p50_ms": lookup["point_lookup"]["p50_ms"],
            "p95_ms": lookup["point_lookup"]["p95_ms"]
        },

        {
            "category": "Lookup",
            "metric": "Indexed lookup",
            "p50_ms": lookup["indexed_lookup"]["p50_ms"],
            "p95_ms": lookup["indexed_lookup"]["p95_ms"]
        },

        {
            "category": "Aggregation",
            "metric": "Node count",
            "p50_ms": aggregation["node_count"]["p50_ms"],
            "p95_ms": aggregation["node_count"]["p95_ms"]
        },

        {
            "category": "Aggregation",
            "metric": "Relationship count",
            "p50_ms": aggregation["relationship_count"]["p50_ms"],
            "p95_ms": aggregation["relationship_count"]["p95_ms"]
        },

        {
            "category": "Mixed workload",
            "metric": "Throughput QPS",
            "p50_ms": "",
            "p95_ms": mixed["throughput"]["qps"]
        }
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "category",
                "metric",
                "p50_ms",
                "p95_ms"
            ]
        )

        writer.writeheader()

        writer.writerows(rows)

    print(
        "Summary created:",
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()