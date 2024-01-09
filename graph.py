from neo4j import GraphDatabase


class Neo4JConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run(
            "CREATE (a:Greeting) "
            "SET a.message = $message "
            "RETURN a.message + ', from node ' + id(a)",
            message=message,
        )
        return result.single()[0]


# connector = Neo4JConnector("bolt://100.27.18.17:7687", "neo4j", "teeth-cellar-dose")
connector = Neo4JConnector("bolt://127.0.0.1:7689", "neo4j", "db_is_awesom3")
connector.print_greeting("hello y'all")
connector.close()
