import time
from neo4j import GraphDatabase

class CypherAdapter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run(self, query, **params):
        with self.driver.session() as s:
            return list(s.run(query, **params))

    def write_batch(self, query, rows):
        with self.driver.session() as s:
            s.run(query, rows=rows).consume()

    def timed(self, query, **params):
        t0 = time.perf_counter()
        self.run(query, **params)
        return (time.perf_counter() - t0) * 1000
