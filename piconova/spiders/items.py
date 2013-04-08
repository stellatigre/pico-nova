# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class Torrent(Item):
    title = Field()
    torrent = Field()
    magnet = Field()
    updated = Field()
    added = Field()
    uploader = Field()
    seeds = Field()
    leech = Field()
    size = Field()
    category = Field()
    visit_id = Field()
    visited = Field()
