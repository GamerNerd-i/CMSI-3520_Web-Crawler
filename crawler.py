import mechanicalsoup as ms
import redis
import configparser
from elasticsearch import Elasticsearch, helpers
from neo4j import GraphDatabase
from graph import Neo4JConnector


class HSWikiCrawler:
    def __init__(self, neo_inputs):
        self.neo_inputs = neo_inputs
        self.browser = ms.StatefulBrowser()

        self.r = redis.Redis()
        self.r.flushall()

        self.wiki_domain = "https://hearthstone.wiki.gg"

        # # Initialize Elasticsearch

        # config = configparser.ConfigParser()
        # config.read("example.ini")
        # print(config.read('example.ini')) # if loaded should print => ['example.ini']
        # self.es = Elasticsearch(
        #     cloud_id=config["ELASTIC"]["cloud_id"],
        #     http_auth=(config["ELASTIC"]["user"], config["ELASTIC"]["password"]),
        # )

    def continuous_crawl(self, start_url, target):
        if start_url.index(self.wiki_domain) != 0:
            print("Invalid URL. Please use a url from the domain: " + self.wiki_domain)
            return

        neo = Neo4JConnector(**self.neo_inputs)
        neo.flush_db()

        self.r.lpush("links", start_url)

        # Start crawl
        while link := self.r.rpop("links"):
            # crawl(browser, r, es, neo, link)
            self.crawl(neo, link)
            if target in str(link).lower():
                break

        # Close connection to Neo4j
        neo.close()

    def crawl(self, neo, url):
        print("Downloading url: " + url)
        self.browser.open(url)

        # # Cache page to elasticsearch
        # write_to_elastic(url, str(browser.page))

        print("Parsing for more links...")
        a_tags = self.browser.page.find_all("a")
        hrefs = [a.get("href") for a in a_tags]

        print("Filtering wiki-only links...")
        links = [self.wiki_domain + a for a in hrefs if a and a.startswith("/wiki/")]

        print("Pushing links onto Redis...")
        self.r.lpush("links", *links)

        print("Adding links to neo4j...")
        neo.add_links(url, links)

        print("Done!\n")

    # def write_to_elastic(url, html):
    #     # because Redis stores strings as ByteStrings,
    #     # we must decode our url into a string of a specific encoding
    #     # for it to be valid JSON
    #     url = url.decode("utf-8")
    #     self.es.index(index="webpages", document={"url": url, "html": html})
