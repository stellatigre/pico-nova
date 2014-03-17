from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as Linx
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from picolib import PicoSpider
from items import Torrent
import re

class KattSpider(PicoSpider):

    name = "katt"
    start_urls = ["http://ka.tt", "http://kat.ph", "http://kickass.to"]
    allowed_domains = ["ka.tt", "kat.ph", "kickass.to"]

    deny_rules = ('/search/*', 'utorrent.btsearch', '/blog/*', '/hourlydump.txt.gz',
	      '/user/*', '/community/*', '/comments/*', '/bookmarks/*', '/images/*')

    torrent_links = '/*.html'
    category_links = ('ka.tt/*/','kickass.to/*/')

    spider_cookies = {
	'user_legal_age' : 'yes'	    # Try to make sure adult pages are scraped too
    }

    rules = (	
	Rule(Linx(allow=torrent_links, deny=deny_rules, allow_domains=allowed_domains, unique=True), 
	    callback='parse_katt_torrent', follow=True),
	
	Rule(Linx(allow=category_links, deny=deny_rules, allow_domains=allowed_domains, unique=True),
	    callback='parse_category', follow=True)
    )

    xpath_dict = {			    # xpaths are tried in the order listed in their array,
	'title': ['//title/text()',],						# so order matters.
	'torrent': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/a[2]/@href',
		    '//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/a[2]/@href',
		    '//*[@id="mainDetailsTable"]/tr/td[1]/div[4]/a[2]/@href'],
	'magnet': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[4]/a[1]/@href',
		   '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/a[1]/@href',
		   '//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/a[1]/@href',
		   '/html/body/div/div/div[5]/table/tr/td/div[4]/a/@href'],
	'seeds': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/div[1]/strong/text()',
		  '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/div[1]/strong/text()'],
	'leech': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[2]/div[2]/strong/text()',
		  '//*[@id="mainDetailsTable"]/tr/td[1]/div[3]/div[2]/strong/text()'],
	'size': ['//*[@id="tab-main"]/div[4]/span/text()[1]', '//*[@id="tab-main"]/div[3]/span/text()[1]',
		 '//*[@id="tab-main"]/div[3]/span/a/text()', '//*[@id="tab-main"]/div[5]/span/text()[1]'],
	'added': ['//*[@id="mainDetailsTable"]/tr/td[1]/div[6]/text()[1]',
		  '//*[@id="mainDetailsTable"]/tr/td[1]/div[7]/text()[1]']
    }

    def size_with_unit(self, raw_size, response):	
	size = re.sub(' \(Size: ', '', str(raw_size)) # removing unneeded labels from the size text

	size_unit = ''
	size_unit_paths = ['//*[@id="tab-main"]/div[4]/span/span[2]/text()',   # the "MB"/"GB" from the
			   '//*[@id="tab-main"]/div[3]/span/span[2]/text()',   # size is in another div.
			   '//*[@id="tab-main"]/div[3]/span/a/span[2]/text()', # This finds that.
			   '//*[@id="tab-main"]/div[5]/span/span[2]/text()']

	hxs = HtmlXPathSelector(response)	    
	for xp in size_unit_paths:
	    size_unit = hxs.select(xp).extract()	    # TODO: Fix deprecation warnings here
	    if size_unit != []:
		break

	return str(size) + str(size_unit[0])			# returns strings like "240.32 MB"

    def trim_added(self, raw_added):				# Massage 'added on' dates
	added = re.sub('\nAdded on ', '' , str(raw_added))	# into a regular format,
	added = re.sub(' by ', '' , added)			# without extra words in it.
	added = re.sub(' in ', '' , added)			
	return added 

    def trim_title(self, raw_title):				# These 2 strings are part of
	title = re.sub('Download ', '' , raw_title)		    # every title on the site.
	title = re.sub('Torrent - KickassTorrents', '', title)	    # This strips them out.
	return title						    

    def parse_katt_torrent(self, response):
	page = Torrent()
	self.try_xpaths(page, self.xpath_dict, response)    # actual scraping mostly happens here
	self.singular(page)				    # turns lists of 1 to single values 

	page['size']  = self.size_with_unit(page['size'], response)	
	page['title'] = self.trim_title(page['title'])		# cleanup data, before sending to	
	page['added'] = self.trim_added(page['added'])		# item pipeline to be stored
	
	return page


spider = KattSpider()
