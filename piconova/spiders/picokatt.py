from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as SLE
from scrapy.contrib.spiders import Rule
from picolib import PicoSpider
from items import Torrent
import re

class KattSpider(PicoSpider):

	name = "katt"
	start_urls = ["http://ka.tt", "http://kat.ph"]
	allowed_domains = ["ka.tt", "kat.ph", "kickass.to"]

	deny_rules = ('/search/*', 'utorrent.btsearch', '/blog/*', '/hourlydump.txt.gz',
                  '/user/*', '/community/*', '/comments/*', '/bookmarks/*')
	tor_links = '/*.html'

	rules = (
        Rule(SLE(allow=tor_links, deny=deny_rules), callback='parse_katt_torrent', follow=True),
        Rule(SLE(allow=('ka.tt/*/','kickass.to/*/',), deny=deny_rules), callback='parse_category', follow=True))

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
		'size': ['//*[@id="tab-main"]/div[4]/span/text()[1]', '//*[@id="tab-main"]/div[3]/span/text()[1]',
				 '//*[@id="tab-main"]/div[3]/span/a/text()'],
		'added': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[6]/text()[1]',
				  '//*[@id="mainDetailsTable"]/tr/td[1]/div[7]/text()[1]'],
	}

	def trim_size(self, raw_size):
		non_decimal = re.compile(r'[^\d.]+')		# Removing irrelevant alphanumeric chars
		size = non_decimal.sub('', str(raw_size))
		return size

	def trim_added(self, raw_added):
		added = re.sub('\nAdded on ', '' , str(raw_added))
		added = re.sub(' by ', '' , added)
		added = re.sub(' in ', '' , added)
		return added 

	def trim_title(self, raw_title):
		title = re.sub('Download ', '' , raw_title)
		title = re.sub('Torrent - KickassTorrents', '', title)
		return title

	def parse_katt_torrent(self, response):
		page = Torrent()
		self.try_xpaths(page, self.xpath_dict, response)
		self.singular(page)

		page['size']  = self.trim_size(page['size'])	# cleanup before sending into item pipeline
		page['added'] = self.trim_added(page['added'])
		page['title'] = self.trim_title(page['title'])

		return page

spider = KattSpider()
