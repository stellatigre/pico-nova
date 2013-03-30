from scrapy.spider   import BaseSpider
from scrapy.contrib.spiders   import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.http import Request
from items import Torrent
import celery

def make_requests_from_url(url):
    return Request(url, dont_filter=False, meta = {'start_url': url})

def get_reqs(url_list): 
	for next in url_list: return next.url		
			
class PicoSpider(CrawlSpider):
	name = "fenopico"
	start_urls = ["http://fenopy.se"]
	allowed_domains=["fenopy.se"]

	rules = (Rule(SgmlLinkExtractor(allow=('/torrent/',),deny=('/download.torrent')),callback='parse_torrent' , follow=True),
			 #Rule(SgmlLinkExtractor(allow=('/sub/',),),callback='parse_subcategory', follow=True),
			 Rule(SgmlLinkExtractor(allow=('/category/',),),callback='parse_category', follow=True))

		# in this one, we're not making any requests, just links		
	def parse_category(self, response):
			tlx = SgmlLinkExtractor(allow='/torrent/',deny='/download.torrent')
			torrents = tlx.extract_links(response)
			for t in torrents:
				req = make_requests_from_url(t.url)
				return req
	
		#make torrent page requests from subcategories
	def parse_subcategory(self, response):
			slx = SgmlLinkExtractor()
			sub_list = slx.extract_links(response)
			sub_req= get_reqs(sub_list)		
			m = make_requests_from_url(sub_req)
			return m			
		
		# actual h33t torrent pages scraped here
	def parse_torrent(self, response):
			hxs = HtmlXPathSelector(response)
			page = Torrent()
			
			# if there's 1 or less seeders, who cares?
			if hxs.select('//*[@id="torrent"]/div[2]/div/dl/dt[1]/text()'):
				if eval(hxs.select('//*[@id="torrent"]/div[2]/div/dl/dt[1]/text()').extract()[0]) <= 1: 
					print'Not really seeded... discarded.'				
					return None

			page['torrent'] = hxs.select('//*[@id="torrent"]/div[2]/div/div[1]/a[3]/@href').extract()
			if not page['torrent'] :
                                page['torrent'] = hxs.select('//*[@id="torrent"]/div[1]/div/div[1]/a[3]/@href').extract() 
			
			page['magnet'] = hxs.select('//*[@id="torrent"]/div[2]/div/div[1]/a[2]/@href').extract()
			if not page['magnet'] :
                                page['magnet'] = hxs.select('//*[@id="torrent"]/div[1]/div/div[1]/a[2]/@href').extract()
			
			page['title']   = hxs.select('//title/text()').extract()		
			
			page['seeds']	= hxs.select('//*[@id="torrent"]/div[2]/div/dl/dt[1]/text()').extract()
			if not page['seeds'] : 
				page['seeds'] = hxs.select('//*[@id="torrent"]/div[1]/div/dl/dt[1]/text()').extract()
			
			page['size']    = hxs.select('//*[@id="torrent"]/div[2]/div/dl/dt[3]/text()').extract()			
			if not page['size'] :
                                page['size'] = hxs.select('//*[@id="torrent"]/div[1]/div/dl/dt[3]/text()').extract() 

			#page['added'] = hxs.select(
			#'/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[7]/td[2]/text()').extract()	
			
			#if page['updated']: del page['updated'][0]
	
			return page

spider = PicoSpider()	
