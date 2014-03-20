from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as Linx
from picolib import PicoSpider

class PirateSpider(PicoSpider):
    
    name = "picobay"
    start_urls = ["http://thepiratebay.se/browse"]
    allowed_domains = ["thepiratebay.se"]

    torrent_links = ('/torrent/',)
    category_links = ('/browse/*/*/7', '/browse/') 
    deny_rules = ('/img*', '/%0Ahttp://*')

    xpath_dict = {
	#'title'    : ('//*[@id="title"]'),
	'seeds'    : ('//*[@id="details"]/dl[1]/dd[7]/text()', 
		      '//*[@id="details"]/dl[2]/dd[3]/text()',
		      '//*[@id="details"]/dl[1]/dd[8]//text()'),
	'magnet'   : ('//*[@id="details"]/div[3]/a[1]/@href',
		      '//*[@id="details"]/div[4]/a/@href',
		      '/html/body/div[3]/div[2]/div/div/div/div[2]/div[10]/a/@href'),
	'torrent'  : ('//*[@id="details"]/div[4]/a[2]/@href',
		      '//*[@id="details"]/div[3]/a[2]/@href'),
	#'category' : ('//*[@id="details"]/dl[1]/dd[1]/a'),
	'leech'    : ('//*[@id="details"]/dl[1]/dd[9]/text()',
		      '//*[@id="details"]/dl[2]/dd[4]/text()'),
	'size'     : ('//*[@id="details"]/dl[1]/dd[3]/text()',),
	'added'    : ('//*[@id="details"]/dl[1]/dd[5]/text()',
		      '//*[@id="details"]/dl[2]/dd[1]/text()'),
	'uploader' : ('//*[@id="details"]/dl[1]/dd[6]/a/text()',
		      '//*[@id="details"]/dl[2]/dd[2]/a/text()')
    }		

    rules = ( 
	Rule(Linx(allow=torrent_links,), callback='parse_torrent', follow=True),
	Rule(Linx(allow=category_links,), callback='parse_category', follow=True)
    )

spider = PirateSpider()

