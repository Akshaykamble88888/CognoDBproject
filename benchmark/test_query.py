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


with driver.session() as session:

    result = session.run(
        "RETURN 'Hello CognoDB' AS message"
    )

    record = result.single()

    print(record["message"])


driver.close()