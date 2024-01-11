import mechanicalsoup as ms
import redis
import configparser
from elasticsearch import Elasticsearch, helpers
from neo4j import GraphDatabase
from graph import Neo4JConnector


def write_to_elastic(es, url, html):
    # because Redis stores strings as ByteStrings,
    # we must decode our url into a string of a specific encoding
    # for it to be valid JSON
    url = url.decode("utf-8")
    es.index(index="webpages", document={"url": url, "html": html})


# def crawl(browser, r, es, neo, url):
def crawl(browser, r, neo, url):
    # Download url
    print("Downloading url")
    browser.open(url)

    # # Cache page to elasticsearch
    # write_to_elastic(es, url, str(browser.page))

    # Parse for more urls
    print("Parsing for more links")
    a_tags = browser.page.find_all("a")
    hrefs = [a.get("href") for a in a_tags]
    page_title = browser.page.find("title").get_text()

    # Filter ONLY for Hearthstone Wiki pages
    wiki_domain = "https://hearthstone.wiki.gg"
    links = [wiki_domain + a for a in hrefs if a and a.startswith("/wiki/")]

    # Put urls in Redis queue
    # create a linked list in Redis, call it "links"
    print("Pushing links onto Redis")
    r.lpush("links", *links)

    # Add links to Neo4J graph
    print("Adding links to neo4j")
    neo.add_links(url, page_title, links)


### MAIN ###

# Initialize Neo4j
neo = Neo4JConnector("bolt://44.199.254.99:7687", "neo4j", "additions-weeks-echoes")
neo.flush_db()

# # Initialize Elasticsearch
# config = configparser.ConfigParser()
# config.read("example.ini")
# print(config.read('example.ini')) # if loaded should print => ['example.ini']
# es = Elasticsearch(
#     cloud_id=config["ELASTIC"]["cloud_id"],
#     http_auth=(config["ELASTIC"]["user"], config["ELASTIC"]["password"]),
# )

# Initialize Redis
r = redis.Redis()
r.flushall()

# Initialize MechanicalSoup headless browser
browser = ms.StatefulBrowser()

# Add root url as the entrypoint to our crawl
start_url = "https://hearthstone.wiki.gg/wiki/Hearthstone_Wiki"
r.lpush("links", start_url)

# Start crawl
while link := r.rpop("links"):
    # crawl(browser, r, es, neo, link)
    crawl(browser, r, neo, link)
    if "justicar" in str(link).lower():
        break

# Close connection to Neo4j
neo.close()
