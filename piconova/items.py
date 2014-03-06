from scrapy.item import Item, Field

class Torrent(Item):
	title   = Field()
	torrent = Field()
	magnet  = Field()
	updated = Field()
	added   = Field()		
	seeds   = Field()
	size    = Field()
	visit_id = Field()
	visit_status = Field()
