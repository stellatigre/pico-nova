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
	name = "picoh33t"
	start_urls = ["http://h33t.com"]
	allowed_domains=["h33t.com"]

	rules = (Rule(SgmlLinkExtractor(allow=('/torrent/',),),callback='parse_h33t_torrent' , follow=True),
			 #Rule(SgmlLinkExtractor(allow=('/sub/',),),callback='parse_subcategory', follow=True),
			 Rule(SgmlLinkExtractor(allow=('/category/',),),callback='parse_h33t_category', follow=True))

		# in this one, we're not making any requests, just links		
	def parse_h33t_category(self, response):
			tlx = SgmlLinkExtractor(allow='/torrent/')
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
	def parse_h33t_torrent(self, response):
			hxs = HtmlXPathSelector(response)
			page = Torrent()
			
			# if there's 1 or less seeders, who cares?
			#if eval(hxs.select('//*[@id="seedsleechers"]//text()').extract()[0]) <= 1: 
			#	print'Not really seeded... discarded.'				
			#	return None

			page['torrent'] = hxs.select(
			'/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[2]/td[2]/table/tr[1]/td[2]/div/a/@href').extract()
			
			page['magnet']  = hxs.select(
			'/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[2]/td[2]/table/tr[1]/td[3]/div/a/@href').extract()
			
			page['title']   = hxs.select('//title/text()').extract()
			page['updated'] = hxs.select('//*[@id="trackers"]/table/tr[*]/td[5]/text()').extract()		
			page['seeds']	= hxs.select('//*[@id="trackers"]/table/tr[*]/td[2]/span/text()').extract()

			page['size']    = hxs.select(
			'/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[5]/td[2]/text()').extract()			
			
			page['added']   = hxs.select(
			'/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[7]/td[2]/text()').extract()	
			
			if page['updated']: del page['updated'][0]
	
			return page

spider = PicoSpider()	
