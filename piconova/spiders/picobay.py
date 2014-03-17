from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as SLE
from items import Torrent
from picolib import PicoSpider
import re

class PirateSpider(PicoSpider):
    
    name = "picobay"
    start_urls = ["http://thepiratebay.se/browse"]
    allowed_domains = ["thepiratebay.se"]

    tor_links = '/torrent/'
    deny_rules = ('/img*', '/%0Ahttp://*')

    xpath_dict = {
	'title'    : ('/html/body/div[2]/div[2]/div/div/div/div/text()[0]',
		      '//*[@id="title"]'),
	'seeds'    : ('//*[@id="details"]/dl[1]/dd[7]/text()', 
		      '//*[@id="details"]/dl[2]/dd[3]/text()',
		      '//*[@id="details"]/dl[1]/dd[8]//text()'),
	'magnet'   : ('//*[@id="details"]/div[3]/a[1]/@href',
		      '//*[@id="details"]/div[4]/a/@href',
		      '/html/body/div[3]/div[2]/div/div/div/div[2]/div[10]/a/@href'),
	'torrent'  : ('//*[@id="details"]/div[4]/a[2]/@href',
		      '//*[@id="details"]/div[3]/a[2]/@href'),
	'leech'    : ('//*[@id="details"]/dl[1]/dd[9]/text()',
		      '//*[@id="details"]/dl[2]/dd[4]/text()'),
	'size'     : ('//*[@id="details"]/dl[1]/dd[3]/text()',),
	'added'    : ('//*[@id="details"]/dl[1]/dd[5]/text()',
		      '//*[@id="details"]/dl[2]/dd[1]/text()'),
	'uploader' : ('//*[@id="details"]/dl[1]/dd[6]/a/text()',
		      '//*[@id="details"]/dl[2]/dd[2]/a/text()')
    }		
																			    
    rules = (
	Rule(SLE(allow=('/torrent/',),), callback='parse_tpb_torrent', follow=True),
	Rule(SLE(allow=('/browse/*/*/7',),), callback='tpb_category_org', follow=True),
	Rule(SLE(allow=('/browse/',),), callback='parse_category', follow=True)
    )

    # make torrent page requests from subcategories
    def tpb_category_org(self, response):
	slx = SgmlLinkExtractor()
	sub_list = slx.extract_links(response)
	sub_req = get_reqs(sub_list)
	m = self.make_requests_for_url(sub_req)
	return m
    
    def clean_leeches(self, leeches):
	non_decimal = re.compile(r'[^\d.]+')
	leeches = non_decimal.sub('', leeches)
	return leeches

    def parse_tpb_torrent(self, response):
	page = Torrent()
	self.try_xpaths(page, self.xpath_dict, response)
	self.singular(page)

	page['magnet'] = page['magnet'][0]
	page['leech'] = self.clean_leeches(page['leech'])
	
	return page

spider = PirateSpider()

