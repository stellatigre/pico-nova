from scrapy.item import Item, Field

class Torrent(Item):
	title    = Field()
	torrent  = Field()
	magnet   = Field()
	updated  = Field()
	added    = Field()		
	seeds    = Field()
	leeches  = Field()
	size     = Field()
	uploader = Field()
	visit_id = Field()
	visited  = Field()
