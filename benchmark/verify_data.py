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
        "MATCH (n:Person) RETURN count(n) AS count"
    )

    node_count = result.single()["count"]

    result = session.run(
        "MATCH ()-[r:KNOWS]->() RETURN count(r) AS count"
    )

    relationship_count = result.single()["count"]


print("Nodes in CognoDB:", node_count)
print(
    "Relationships in CognoDB:",
    relationship_count
)


driver.close()