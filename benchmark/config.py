import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    "cognodb": {
        "uri": os.getenv("COGNODB_URI"),
        "user": os.getenv("COGNODB_USER", "cognodb"),
        "password": os.getenv("COGNODB_PASSWORD"),
    },
    "neo4j": {
        "uri": os.getenv("NEO4J_URI"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD"),
    },
    "memgraph": {
        "uri": os.getenv("MEMGRAPH_URI"),
        "user": os.getenv("MEMGRAPH_USER", ""),
        "password": os.getenv("MEMGRAPH_PASSWORD", ""),
    },
}
