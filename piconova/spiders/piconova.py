from scrapy.spider   import BaseSpider
from scrapy.contrib.spiders   import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.http import Request
from items import Torrent

def make_requests_from_url(url):
    return Request(url, dont_filter=False, meta = {'start_url': url})

def get_reqs(url_list): 
	for next in url_list: return next.url		
			
class PicoSpider(CrawlSpider):
	name = "piconova"
	start_urls = ["http://www.mininova.org"]
	allowed_domains=["www.mininova.org"]

	rules = (Rule(SgmlLinkExtractor(allow=('/tor/',),),callback='parse_mn_torrent' , follow=True),
			 Rule(SgmlLinkExtractor(allow=('/sub/',),),callback='parse_subcategory', follow=True),
			 Rule(SgmlLinkExtractor(allow=('/cat/',),),callback='parse_mn_category', follow=True))

		# in this one, we're not making any requests, just links		
	def parse_mn_category(self, response):
			slx = SgmlLinkExtractor(allow='/sub/')
			sub_cats = slx.extract_links(response)
			for s in sub_cats:
				req = make_requests_from_url(s.url)
				return req
	
		#make torrent page requests from subcategories
	def parse_subcategory(self, response):
			slx = SgmlLinkExtractor()
			sub_list = slx.extract_links(response)
			sub_req= get_reqs(sub_list)		
			m = make_requests_from_url(sub_req)
			return m			
		
		# actual Mininova torrent pages scraped here
	def parse_mn_torrent(self, response):
			hxs = HtmlXPathSelector(response)
			page = Torrent()
			
			# if there's 1 or less seeders, who cares?
			if eval(hxs.select('//*[@id="seedsleechers"]//text()').extract()[0]) <= 1: 
				print'Not really seeded... discarded.'				
				return None
			# These if/elses are needed due to some div they add on music pages
			page['torrent'] = hxs.select('/html/body/div[3]/div[2]/div/h2/a/@href').extract()
			if page['torrent']: pass
			else : page['torrent']= hxs.select('/html/body/div[3]/div[2]/h2/a/@href').extract()

			page['magnet']  = hxs.select('/html/body/div[3]/div[2]/div/a[2]/@href').extract()
			if page['magnet'] : pass
			else:  page['magnet'] = hxs.select('/html/body/div[3]/div[2]/a[2]/@href').extract()	

			# The rest have static Xpaths
			page['title']   = hxs.select('//title/text()').extract()
			page['updated'] = hxs.select('//*[@id="lastupdated"]/text()').extract()		
			page['seeds']	= hxs.select('//*[@id="seedsleechers"]//text()').extract()
			page['size']    = hxs.select('/html/body/div[3]/div[4]/p[3]//text()').extract()				
			page['added']   = hxs.select('/html/body/div[3]/div[4]/p[4]//text()').extract()		
		
			# cleanup, removing excess data		
			if len(page['torrent']) > 1:
				del(page['torrent'][1])
			del(page['added'][:2])
			del(page['size' ][:2])
		
			return page

spider = PicoSpider()	
