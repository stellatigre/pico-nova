from picolib import PicoSpider

class H33tSpider(PicoSpider):
	
    name = "picoh33t"
    start_urls = ["http://h33t.to"]
    allowed_domains = ["h33t.to"]

    torrent_links = '/torrent/*'
    category_links = '/category/'
    deny_rules = ('/member/*', 'fr33sp33k',)

    xpath_dict = {
	'torrent' : ('/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[2]/td[2]/table/tr[1]/td[2]/div/a/@href',), 
	'magnet'  : ('/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[2]/td[2]/table/tr[1]/td[3]/div/a/@href',),
	'title'   : ('//title/text()',), 
	'updated' : ('//*[@id="trackers"]/table/tr[*]/td[5]/text()',),
	'seeds'   : ('//*[@id="trackers"]/table/tr[*]/td[2]/span/text()',),
	'size'    : ('//*[@id="trackers"]/table/tr[*]/td[2]/span/text()',),
	'added'   : ('/html/body/table/tr/td/table/tr[3]/td/table/tr/td/div/table[1]/tr[7]/td[2]/text()',),
    }


spider = PicoSpider()
