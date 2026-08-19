import os
import json

from dotenv import load_dotenv
from neo4j import GraphDatabase

from benchmark import run_query


load_dotenv()


URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


START_NODES_FILE = "start_nodes.json"
RESULT_FILE = "results/cognodb_lookup.json"


POINT_LOOKUP_QUERY = """
MATCH (p:Person {id: $start_id})
RETURN p
"""


INDEXED_LOOKUP_QUERY = """
MATCH (p:Person {id: $start_id})
RETURN p
"""


def load_start_nodes():

    with open(
        START_NODES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def benchmark_lookup(
    session,
    query,
    start_nodes
):

    timings = []

    # Warm-up
    for start_id in start_nodes[:10]:

        session.run(
            query,
            start_id=start_id
        ).consume()

    # Actual measurements
    for start_id in start_nodes:

        result = run_query(
            session=session,
            query=query,
            parameters={
                "start_id": start_id
            },
            iterations=1,
            warmup=0
        )

        timings.append(
            result["avg_ms"]
        )

    timings.sort()

    p50_index = int(
        0.50 * (len(timings) - 1)
    )

    p95_index = int(
        0.95 * (len(timings) - 1)
    )

    return {
        "p50_ms": timings[p50_index],
        "p95_ms": timings[p95_index],
        "min_ms": min(timings),
        "max_ms": max(timings),
        "avg_ms": sum(timings) / len(timings),
        "iterations": len(timings)
    }


def main():

    start_nodes = load_start_nodes()

    print(
        "Start nodes loaded:",
        len(start_nodes)
    )

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    results = {}

    try:

        with driver.session() as session:

            print()
            print("Running point lookup...")

            results["point_lookup"] = benchmark_lookup(
                session,
                POINT_LOOKUP_QUERY,
                start_nodes
            )

            print(
                results["point_lookup"]
            )

            print()
            print("Running indexed lookup...")

            results["indexed_lookup"] = benchmark_lookup(
                session,
                INDEXED_LOOKUP_QUERY,
                start_nodes
            )

            print(
                results["indexed_lookup"]
            )

    finally:

        driver.close()

    os.makedirs(
        "results",
        exist_ok=True
    )

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print()
    print(
        "Lookup results saved to:"
    )
    print(RESULT_FILE)


if __name__ == "__main__":
    main()