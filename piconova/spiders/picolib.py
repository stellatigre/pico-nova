from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as Linx
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from items import Torrent

class PicoSpider(CrawlSpider):
	
    name = "picospider"
    
    xpath_dict = {}		# When subclassed for real use, fill in dictionary of xpaths
    spider_cookies = {}		# optional - use if needed
    allowed_domains = []	# domains you want to both stay on and consider for links 
    
    torrent_links = ()		# regex(es) to match torrent page links
    category_links = ()		# links to get other torrent links from
    deny_rules = ()		# the spider will ignore all these when looking for links

    rules = ()

    def singular(self, torrent):			# turn lists of length == 1
	for field in torrent:				# into single values 
	    if len(torrent[field]) == 1:
		torrent[field] = torrent[field][0]
 
    def try_xpaths(self, Torrent, xp_dict, response):	# the tuples of xpaths in xpath_dict
	hxs = HtmlXPathSelector(response)		# should go in order from first->last
	for field in xp_dict:				    # to be tried on each page
	    for xp in xp_dict[field]:
		Torrent[field] = hxs.select(xp).extract()
		if Torrent[field]:				# if we got a value, 
		    break					# move on to the next field

    def make_requests_for_url(self, link):
	yield Request(link.url, dont_filter=False, meta={'start_url': link.url}, cookies=self.spider_cookies)
	
    def make_all_requests(self, Links):
	map(self.make_requests_for_url, Links)

    def get_links(self, response, allowed):	
	tlx = Linx(allow=allowed, deny=self.deny_rules)
	links = tlx.extract_links(response)
	yield links

    def parse_category(self, response):
	links = self.get_links(response, self.torrent_links+self.category_links)
	self.make_all_requests(links)	

    def parse_torrent(self, response):
	page = Torrent()
	self.try_xpaths(page, self.xpath_dict, response)    # actual value extraction happens here
    	self.singular(page)
	yield page

