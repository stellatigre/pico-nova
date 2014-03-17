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
    
    torrent_links = ('/*.html')		# regex(es) to match torrent page links
    category_links = ()		# links to get other torrent links from
    deny_rules = ()		# the spider will ignore all these when looking for links
    
    torrent_callback = 'parse_torrent'		# setup this way to enable easy override
    category_callback = 'parse_category'	# of the the Rule callbacks

    # Often we'll overwrite these rules but they are good defaults
    rules = (
	# find links to torrent pages, and scrapes the actual torrent info on response	
	Rule(
	    Linx(allow=torrent_links, deny=deny_rules, allow_domains=allowed_domains, unique=True), 
	    callback=torrent_callback, follow=True
	),
	# find links we can get other links from, and gets links from them on response
	Rule(
	    Linx(allow=category_links, deny=deny_rules, allow_domains=allowed_domains, unique=True),
	    callback=category_callback, follow=True
	)
    )

    def get_reqs(self, url_list):
	for next in url_list:
	    return next.url

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

    def make_requests_for_url(self, url):
	return Request(url, dont_filter=False, meta={'start_url': url}, cookies=self.spider_cookies)

    # in this one, we're not making any requests, just links
    def parse_category(self, response):
	tlx = Linx(allow=self.torrent_links, deny=self.deny_rules)
	torrents = tlx.extract_links(response)
	for t in torrents:
	    request = self.make_requests_for_url(t.url)
	    return request

    def parse_torrent(self, response):
	page = Torrent()
	self.try_xpaths(page, self.xpath_dict, response)    # actual value extraction happens here
	self.singular(page)
	return page

