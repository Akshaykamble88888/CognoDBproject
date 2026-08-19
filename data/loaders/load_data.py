import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

INPUT_FILE = "../pokec_sample.txt"

BATCH_SIZE = 1000


def create_driver():
    return GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )


def load_nodes(driver):

    print("Loading nodes...")

    nodes = set()

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            source = parts[0]
            target = parts[1]

            nodes.add(source)
            nodes.add(target)

    print("Unique nodes found:", len(nodes))

    node_list = [
        {"id": node_id}
        for node_id in nodes
    ]

    with driver.session() as session:

        for i in range(0, len(node_list), BATCH_SIZE):

            batch = node_list[i:i + BATCH_SIZE]

            session.run(
                """
                UNWIND $nodes AS node
                MERGE (p:Person {id: node.id})
                """,
                nodes=batch
            ).consume()

            print(
                f"Nodes loaded: "
                f"{min(i + BATCH_SIZE, len(node_list))}/"
                f"{len(node_list)}"
            )


def load_relationships(driver):

    print("Loading relationships...")

    relationships = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            source = parts[0]
            target = parts[1]

            relationships.append({
                "source": source,
                "target": target
            })

    print(
        "Relationships found:",
        len(relationships)
    )

    with driver.session() as session:

        for i in range(
            0,
            len(relationships),
            BATCH_SIZE
        ):

            batch = relationships[
                i:i + BATCH_SIZE
            ]

            session.run(
                """
                UNWIND $relationships AS rel

                MATCH (source:Person {id: rel.source})
                MATCH (target:Person {id: rel.target})

                CREATE (source)-[:KNOWS]->(target)
                """,
                relationships=batch
            ).consume()

            print(
                f"Relationships loaded: "
                f"{min(i + BATCH_SIZE, len(relationships))}/"
                f"{len(relationships)}"
            )


def main():

    print("Connecting to CognoDB...")

    driver = create_driver()

    try:

        driver.verify_connectivity()

        print("Connected successfully!")

        load_nodes(driver)

        load_relationships(driver)

        print()
        print("Dataset loading completed!")

    except Exception as error:

        print()
        print("Loading failed:")
        print(error)

    finally:

        driver.close()


if __name__ == "__main__":
    main()