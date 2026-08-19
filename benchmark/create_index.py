import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


try:

    with driver.session() as session:

        session.run("""
            CREATE INDEX person_id_index IF NOT EXISTS
            FOR (p:Person)
            ON (p.id)
        """).consume()

        print("Person.id index created successfully!")


except Exception as error:

    print("Index creation failed:")
    print(error)


finally:

    driver.close()