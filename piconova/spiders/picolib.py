from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from items import Torrent

class PicoSpider(CrawlSpider):
	name = "picospider"
	xpath_dict = {}		# When subclassed for real use, fill in dictionary of xpaths
    	
	def get_reqs(self, url_list):
		for next in url_list:
			return next.url

	def singular(self, torrent):
		for field in torrent:
			if len(torrent[field]) == 1:
				torrent[field] = torrent[field][0]

		
	def try_xpaths(self, Torrent, xp_dict, response): # the tuples of xpaths included in the dict
		hxs = HtmlXPathSelector(response)		# go in order from first to last
		for field in xp_dict:
			for xp in xp_dict[field]:
				Torrent[field] = hxs.select(xp).extract()
				if Torrent[field]:
					break

	def make_requests_for_url(self, url):
		return Request(url, dont_filter=False, meta={'start_url': url})

	# in this one, we're not making any requests, just links
	def parse_category(self, response):
		tlx = SgmlLinkExtractor(allow=self.tor_links, deny=self.deny_rules)
		torrents = tlx.extract_links(response)
		for t in torrents:
			request = self.make_requests_for_url(t.url)
			return request

	parse_subcategory = parse_category;

	def parse_torrent(self, response):
		page = Torrent()
		self.try_xpaths(page, self.xpath_dict, response)
		self.singular(page)
		return page
