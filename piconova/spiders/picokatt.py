from scrapy.contrib.spiders   import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from items import Torrent
from settings import DENY_RULES_KATT
from picolib import PicoSpider, try_xpaths, make_requests_from_url

xpath_dict = {
                'title'   : ('//title/text()',),
                'torrent' : ('//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/a[2]/@href',
                             '//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/a[2]/@href'),
                'magnet'  : ('//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/a[1]/@href',
                             '//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/a[1]/@href'),
                'seeds'   : ('//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/div[1]/strong/text()',
                             '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/div[1]/strong/text()'),
                'leech'   : ('//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/div[2]/strong/text()',
                             '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/div[2]/strong/text()'),
                'size'    : ('//*[@id="first"]/div[4]/span/text()[1]', '//*[@id="first"]/div[3]/span/text()[1]'),
                'added'   : ('//*[@id="mainDetailsTable"]/tr/td[1]/div[6]/text()[1]',),
                }

class KattSpider(PicoSpider):
	
	name = "katt"
	start_urls = ["http://ka.tt", "http://kat.ph"]
	allowed_domains =["ka.tt", "kat.ph"]
	deny_rules = DENY_RULES_KATT
	tor_links = '/*.html'
	
	rules = (Rule(SgmlLinkExtractor(allow=('/*.html',),deny=deny_rules),callback='parse_torrent' , follow=True),
		Rule(SgmlLinkExtractor(allow=('ka.tt/*/',), deny=deny_rules),callback='parse_category', follow=True))			
		
	def parse_torrent(self, response):
			page = Torrent()
			try_xpaths(page, xpath_dict, response)
			return page

spider = KattSpider()
