import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

print("URI:", URI)
print("USERNAME:", USERNAME)
print("DATABASE:", DATABASE)

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    with driver.session(database=DATABASE) as session:
        result = session.run("RETURN 1 AS test")
        record = result.single()

        print("Neo4j connection successful!")
        print("Test result:", record["test"])

finally:
    driver.close()