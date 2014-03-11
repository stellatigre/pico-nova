from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as SLE
from scrapy.contrib.spiders import Rule
from picolib import PicoSpider
from items import Torrent
import re

class KattSpider(PicoSpider):

	name = "katt"
	start_urls = ["http://ka.tt", "http://kat.ph"]
	allowed_domains = ["ka.tt", "kat.ph", "kickass.to"]

	deny_rules = ('/search/*', 'utorrent.btsearch', '/blog/*',
                  '/user/*', '/community/*', '/comments/*', '/show/*')

	rules = (
        Rule(SLE(allow=('/*.html', ), deny=deny_rules), callback='parse_katt_torrent', follow=True),
        Rule(SLE(allow=('ka.tt/*/',), deny=deny_rules), callback='parse_category', follow=True))

	xpath_dict = {
		'title': ['//title/text()',],
		'torrent': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/a[2]/@href',
                    '//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/a[2]/@href'],
		'magnet': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/a[1]/@href',
                   '//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/a[1]/@href'],
		'seeds': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/div[1]/strong/text()',
                  '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/div[1]/strong/text()'],
		'leech': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/div[2]/strong/text()',
                  '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/div[2]/strong/text()'],
		'size': ['//*[@id="tab-main"]/div[4]/span/text()[1]', '//*[@id="tab-main"]/div[3]/span/text()[1]'],
		'added': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[6]/text()[1]',],
	}

	def trim_size(self, raw_page_size):
		non_decimal = re.compile(r'[^\d.]+')		# Removing irrelevant alphanumeric chars
		page_size = raw_page_size[0]
		page_size = non_decimal.sub('', page_size)
		return page_size

	def parse_katt_torrent(self, response):
		page = Torrent()
		self.try_xpaths(page, self.xpath_dict, response)
		
		page['size'] = self.trim_size(page['size'])
		self.singular(page)

		return page

spider = KattSpider()
