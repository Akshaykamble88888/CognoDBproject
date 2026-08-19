import os
import json
import time
import random

from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


START_NODES_FILE = "start_nodes.json"
RESULT_FILE = "results/cognodb_mixed_workload.json"


CONCURRENCY = 10
READ_PERCENTAGE = 70
WRITE_PERCENTAGE = 30
DURATION_SECONDS = 20


def load_start_nodes():

    with open(
        START_NODES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def run_client(
    driver,
    client_id,
    start_nodes
):

    random.seed(42 + client_id)

    reads = 0
    writes = 0
    errors = 0

    end_time = time.time() + DURATION_SECONDS

    while time.time() < end_time:

        try:

            # Decide READ or WRITE
            random_number = random.randint(1, 100)

            with driver.session() as session:

                if random_number <= READ_PERCENTAGE:

                    # READ operation
                    start_id = random.choice(
                        start_nodes
                    )

                    session.run(
                        """
                        MATCH (p:Person {id: $start_id})
                        RETURN p
                        LIMIT 1
                        """,
                        start_id=start_id
                    ).consume()

                    reads += 1

                else:

                    # WRITE operation
                    write_id = (
                        f"client-{client_id}-"
                        f"{random.randint(1, 100)}"
                    )

                    session.run(
                        """
                        MERGE (b:BenchmarkWrite {
                            id: $write_id
                        })
                        SET b.updatedAt = timestamp()
                        """,
                        write_id=write_id
                    ).consume()

                    writes += 1

        except Exception:

            errors += 1

    return {
        "client_id": client_id,
        "reads": reads,
        "writes": writes,
        "errors": errors
    }


def main():

    print("Starting mixed workload benchmark...")
    print()
    print("Concurrency:", CONCURRENCY)
    print("Read percentage:", READ_PERCENTAGE)
    print("Write percentage:", WRITE_PERCENTAGE)
    print("Duration:", DURATION_SECONDS, "seconds")
    print()

    start_nodes = load_start_nodes()

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    start_time = time.perf_counter()

    client_results = []

    try:

        with ThreadPoolExecutor(
            max_workers=CONCURRENCY
        ) as executor:

            futures = []

            for client_id in range(
                CONCURRENCY
            ):

                future = executor.submit(
                    run_client,
                    driver,
                    client_id,
                    start_nodes
                )

                futures.append(future)

            for future in as_completed(futures):

                result = future.result()

                client_results.append(result)

                print(
                    f"Client {result['client_id']} "
                    f"completed | "
                    f"reads={result['reads']} | "
                    f"writes={result['writes']} | "
                    f"errors={result['errors']}"
                )

    finally:

        driver.close()

    end_time = time.perf_counter()

    duration = end_time - start_time

    total_reads = sum(
        result["reads"]
        for result in client_results
    )

    total_writes = sum(
        result["writes"]
        for result in client_results
    )

    total_errors = sum(
        result["errors"]
        for result in client_results
    )

    total_operations = (
        total_reads +
        total_writes
    )

    qps = (
        total_operations / duration
        if duration > 0
        else 0
    )

    results = {

        "configuration": {
            "concurrency": CONCURRENCY,
            "read_percentage": READ_PERCENTAGE,
            "write_percentage": WRITE_PERCENTAGE,
            "duration_seconds": duration
        },

        "operations": {
            "total": total_operations,
            "reads": total_reads,
            "writes": total_writes,
            "errors": total_errors
        },

        "throughput": {
            "qps": qps
        }
    }

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
    print("Mixed workload completed!")
    print()
    print("Total operations:", total_operations)
    print("Read operations:", total_reads)
    print("Write operations:", total_writes)
    print("Errors:", total_errors)
    print("Duration:", round(duration, 2), "seconds")
    print("Throughput:", round(qps, 2), "QPS")
    print()
    print(
        "Results saved to:",
        RESULT_FILE
    )


if __name__ == "__main__":
    main()