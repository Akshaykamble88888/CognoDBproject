import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt+s://db-320f7cf3.databases.cognodb.com",
    auth=("cognodb", "<f06b3228178ab8018817bacf4294983d>"),
)
driver.verify_connectivity()

try:
    driver.verify_connectivity()
    print("Connected to CognoDB successfully!")

except Exception as e:
    print("Connection failed:")
    print(e)

finally:
    driver.close()