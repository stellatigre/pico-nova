from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as SLE
from scrapy.contrib.spiders import Rule
from picolib import PicoSpider


class FenoPico(PicoSpider):
  
    name = "fenopico"
    start_urls = ["http://fenopy.se"]
    allowed_domains = ["fenopy.se"]
    tor_links = ['/torrent/']
    deny_rules = ['/download.torrent']
    cat_links = ['/category/']

    rules = (
        Rule(SLE(allow=tor_links, deny=deny_rules), callback='parse_torrent', follow=True),
        Rule(SLE(allow=cat_links, deny=deny_rules), callback='parse_category', follow=True)
    )

    xpath_dict = {
        'title': ('//*[@id="breadcrumb"]/li[3]/h1/text()',),
        'seeds': ('//*[@id="torrent"]/div[2]/div/dl/dt[1]/text()',
                  '//*[@id="torrent"]/div[1]/div/dl/dt[1]/text()'),
        'torrent': ('//*[@id="torrent"]/div[2]/div/div[1]/a[3]/@href',
                    '//*[@id="torrent"]/div[1]/div/div[1]/a[3]/@href'),
        'magnet': ('//*[@id="torrent"]/div[2]/div/div[1]/a[2]/@href',
                   '//*[@id="torrent"]/div[1]/div/div[1]/a[2]/@href'),
        'size': ('//*[@id="torrent"]/div[2]/div/dl/dt[3]/text()',
                 '//*[@id="torrent"]/div[1]/div/dl/dt[3]/text()')
    }

spider = FenoPico()
