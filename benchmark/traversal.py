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
RESULT_FILE = "results/cognodb_traversal_random.json"


QUERIES = {

    "1-hop": """
        MATCH (p:Person {id: $start_id})
              -[:KNOWS]->(friend)
        RETURN friend
        LIMIT 10
    """,

    "2-hop": """
        MATCH (p:Person {id: $start_id})
              -[:KNOWS]->
              ()-[:KNOWS]->(friend)
        RETURN friend
        LIMIT 10
    """,

    "3-hop": """
        MATCH (p:Person {id: $start_id})
              -[:KNOWS]->
              ()-[:KNOWS]->
              ()-[:KNOWS]->(friend)
        RETURN friend
        LIMIT 10
    """
}


def load_start_nodes():

    with open(
        START_NODES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


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

            for name, query in QUERIES.items():

                print()
                print(
                    f"Running {name} benchmark..."
                )

                timings = []

                # Warm-up
                for start_id in start_nodes[:10]:

                    session.run(
                        query,
                        start_id=start_id
                    ).consume()

                # Actual benchmark
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

                # Calculate percentiles
                timings.sort()

                p50_index = int(
                    0.50 * (len(timings) - 1)
                )

                p95_index = int(
                    0.95 * (len(timings) - 1)
                )

                p50 = timings[p50_index]
                p95 = timings[p95_index]

                result = {
                    "p50_ms": p50,
                    "p95_ms": p95,
                    "min_ms": min(timings),
                    "max_ms": max(timings),
                    "avg_ms": sum(timings) / len(timings),
                    "iterations": len(timings)
                }

                results[name] = result

                print(result)

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
        "Random traversal results saved to:"
    )
    print(RESULT_FILE)


if __name__ == "__main__":
    main()