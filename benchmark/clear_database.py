import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


def main():

    print("Connecting to CognoDB...")

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    try:

        driver.verify_connectivity()

        print("Connected successfully!")

        with driver.session() as session:

            print("Deleting existing benchmark data...")

            session.run(
                """
                MATCH (n)
                DETACH DELETE n
                """
            ).consume()

            print("Old data deleted successfully!")

    except Exception as error:

        print("Database clearing failed:")
        print(error)

    finally:

        driver.close()


if __name__ == "__main__":
    main()