from crawler import HSWikiCrawler

neo4j = ["bolt://44.211.58.176:7687", "neo4j", "columns-rays-launcher"]
crawler = HSWikiCrawler(neo4j)
crawler.continuous_crawl(
    "https://hearthstone.wiki.gg/wiki/Hearthstone_Wiki", "justicar"
)
print("Done!")
