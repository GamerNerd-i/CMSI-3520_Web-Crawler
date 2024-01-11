# cmsi3520 - Databases Makeup

Aidan Dionisio

The web crawler in this repository crawls through the [Hearthstone Wiki](https://hearthstone.wiki.gg/wiki/Hearthstone_Wiki) rather than Wikipedia.

 The [resuling class](crawler.py) has a function that takes in a valid starting link and crawls the website starting from that link searching for some target text. The [main](main.py) file has an example of this functionality, assuming that the neo4j database is active.
