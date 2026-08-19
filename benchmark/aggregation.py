import os
import json
import statistics
import time

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

RESULT_FILE = "results/cognodb_aggregation.json"

QUERIES = {
    "node_count": """
        MATCH (p:Person)
        RETURN count(p) AS total_nodes
    """,

    "relationship_count": """
        MATCH ()-[r:KNOWS]->()
        RETURN count(r) AS total_relationships
    """
}


def percentile(values, percent):

    values = sorted(values)

    index = int(
        (percent / 100) * (len(values) - 1)
    )

    return values[index]


def run_benchmark(session, query):

    # Warm-up
    for _ in range(10):
        session.run(query).consume()

    timings = []

    # 100 actual iterations
    for _ in range(100):

        start = time.perf_counter()

        session.run(query).consume()

        end = time.perf_counter()

        latency_ms = (
            end - start
        ) * 1000

        timings.append(latency_ms)

    return {
        "p50_ms": percentile(timings, 50),
        "p95_ms": percentile(timings, 95),
        "min_ms": min(timings),
        "max_ms": max(timings),
        "avg_ms": statistics.mean(timings),
        "iterations": len(timings)
    }


def main():

    print("Starting aggregation benchmark...")
    print()

    os.makedirs(
        "results",
        exist_ok=True
    )

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    results = {}

    try:

        driver.verify_connectivity()

        print("Connected to CognoDB!")
        print()

        with driver.session() as session:

            for name, query in QUERIES.items():

                print(
                    f"Running {name} benchmark..."
                )

                result = run_benchmark(
                    session,
                    query
                )

                results[name] = result

                print(result)
                print()

    except Exception as error:

        print("Aggregation benchmark failed:")
        print(error)

        return

    finally:

        driver.close()

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

    print("Aggregation benchmark completed!")
    print()
    print(
        "Aggregation results saved to:"
    )
    print(RESULT_FILE)


if __name__ == "__main__":
    main()