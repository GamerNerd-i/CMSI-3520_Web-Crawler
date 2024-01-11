from neo4j import GraphDatabase


class Neo4JConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_links(self, page, title, links):
        with self.driver.session() as session:
            session.execute_write(self._create_links, page, title, links)

    def flush_db(self):
        print("clearing graph db")
        with self.driver.session() as session:
            session.execute_write(self._flush_db)

    @staticmethod
    def _create_links(tx, page, title, links):
        # because Redis stores strings as ByteStrings,
        # we must decode our url into a string of a specific encoding
        # for it to be valid JSON
        page = page.decode("utf-8")
        tx.run("CREATE (:Page { url: $page, title: $title })", page=page, title=title)
        for link in links:
            tx.run(
                "MATCH (p:Page) WHERE p.url = $page "
                "CREATE (:Page { url: $link }) -[:LINKS_TO]-> (p)",
                link=link,
                page=page,
            )

    @staticmethod
    def _flush_db(tx):
        tx.run("MATCH (a) -[r]-> () DELETE a, r")
        tx.run("MATCH (a) DELETE a")


# # connector = Neo4JConnector("bolt://100.27.18.17:7687", "neo4j", "teeth-cellar-dose")
# connector = Neo4JConnector(
#     "bolt://44.199.254.99:7687", "neo4j", "additions-weeks-echoes"
# )
