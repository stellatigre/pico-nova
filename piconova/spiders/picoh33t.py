from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.http import Request
from items import Torrent
from picolib import Picospider


class H33tSpider(PicoSpider):
    name = "picoh33t"
    start_urls = ["http://h33t.com"]
    allowed_domains = ["h33t.com"]

	tor_links = '/torrent/'
	deny_rules = ''

	xpath_dict = {
		'torrent' : ('/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[2]/td[2]/table/tr[1]/td[2]/div/a/@href',), 
		'magnet'  : ('/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[2]/td[2]/table/tr[1]/td[3]/div/a/@href',),
		'title'   : ('//title/text()',), 
		'updated' : ('//*[@id="trackers"]/table/tr[*]/td[5]/text()',),
		'seeds'   : ('//*[@id="trackers"]/table/tr[*]/td[2]/span/text()',),
		'size'    : ('//*[@id="trackers"]/table/tr[*]/td[2]/span/text()',),
		'added'   : ('/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[7]/td[2]/text()',),
	}

    rules = (
        Rule(SgmlLinkExtractor(allow=('/torrent/',),), callback='parse_torrent', follow=True),
        Rule(SgmlLinkExtractor(allow=('/category/',),), callback='parse_category', follow=True)
	)


spider = PicoSpider()
