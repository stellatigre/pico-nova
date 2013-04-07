from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.http import Request
from items import Torrent

xpath_dict = {}

def try_xpaths(Torrent, xp_dict, response):
	hxs = HtmlXPathSelector(response)
        for field in xp_dict:
        	for xp in xp_dict[field]:
                	Torrent[field] = hxs.select(xp).extract()
                        if Torrent[field]: break

def make_requests_from_url(self, url):
                return Request(url, dont_filter=False, meta = {'start_url': url})


class PicoSpider(CrawlSpider):
	name = "picospider"  

	def get_reqs(self, url_list):
        	for next in url_list: return next.url

                # in this one, we're not making any requests, just links                
        def parse_category(self, response):
			print "\n\nDEBUG SWAG PARSE CAT\n\n"
                        tlx = SgmlLinkExtractor(allow=self.tor_links,deny=self.deny_rules)
                        torrents = tlx.extract_links(response)
                        for t in torrents:
                                req = make_requests_from_url(t.url)
                                return req

                #make torrent page requests from subcategories
        def parse_subcategory(self, response):
                        slx = SgmlLinkExtracto(allow=self.tor_links,deny=self.deny_rules)
                        sub_list = slx.extract_links(response)
                        sub_req= get_reqs(sub_list)
                        m = make_requests_from_url(sub_req)
                        return m

	def parse_torrent(self, response):
                page = Torrent()
                try_xpaths(page, self.xpath_dict, response)
                return page
