# Logical workloads. Cypher-compatible databases use these directly.
# ArangoDB needs an AQL translation in its adapter.

CREATE_INDEX = "CREATE INDEX person_id_idx IF NOT EXISTS FOR (p:Person) ON (p.id)"

INSERT_BATCH = """
UNWIND $rows AS row
MERGE (a:Person {id: row.src})
MERGE (b:Person {id: row.dst})
MERGE (a)-[:KNOWS]->(b)
"""

Q_1HOP = """
MATCH (a:Person {id: $id})-[:KNOWS]->(b)
RETURN count(b) AS n
"""

Q_2HOP = """
MATCH (a:Person {id: $id})-[:KNOWS]->()-[:KNOWS]->(c)
RETURN count(c) AS n
"""

Q_3HOP = """
MATCH (a:Person {id: $id})-[:KNOWS]->()-[:KNOWS]->()-[:KNOWS]->(d)
RETURN count(d) AS n
"""

Q_POINT = """
MATCH (p:Person {id: $id})
RETURN p.id AS id
"""

Q_FILTER = """
MATCH (p:Person)
WHERE p.id >= $lo AND p.id < $hi
RETURN count(p) AS n
"""

Q_AGG = """
MATCH (p:Person)-[:KNOWS]->()
RETURN p.id % 10 AS bucket, count(*) AS n
ORDER BY bucket
"""
