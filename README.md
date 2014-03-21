pico-nova
=========

Scrapers / crawlers for 5 popular public BitTorrent sites: 

http://kickass.to, http://mininova.org, http://thepiratebay.se, http://h33t.to, & http://fenopy.se . 

Uses the Scrapy web scraping framework for Python 2.7 - http://scrapy.org/


Available Spiders
-----------------

The most developed spider is ["katt"](/piconova/spiders/picokatt.py), for http://kickass.to . It's been tuned to give very reliable data.  

The other 4 spiders have a lesser degree of specialization. All of the spiders subclass the "PicoSpider" found in ["picolib.py"](/piconova/spiders/picolib.py), and pass in data about their specific site to pre-established variables from the PicoSpider : such as regular expressions to match links against, and a dictionary of Xpaths for scraping their torrent pages.  Some override the default callbacks for parsing pages to deal with site-specific issues / data cleanup.  

To crawl a domain (given that the data store / MongoDB connection is setup), run this from anywhere in the repo directory:

    scrapy crawl <spider name>
    
### Domain   :  Spider Name ###

kickass.to : ["katt"](/piconova/spiders/picokatt.py)

h33t.to :  ["picoh33t"](/piconova/spiders/picoh33t.py)

thepiratebay.se : ["picobay"](/piconova/spiders/picobay.py)

mininova.org : ["piconova"](/piconova/spiders/piconova.py)

fenopy.se : ["fenopico"](/piconova/spiders/fenopico.py)


Dependencies & Installation
--------------------------

* Python 2.7
* Scrapy - depends on `pip`, `lxml` , `OpenSSL` ; see http://doc.scrapy.org/en/latest/intro/install.html for more on installing scrapy


Data Store Setup / Use (MongoDB)
--------------------------------

This spider stores scraped torrent objects in a MongoDB collection.  To setup:

1) Install MongoDB for your platform of choice if not installed.  http://docs.mongodb.org/manual/installation/

2) Start a `mongod` instance for the spider to bind to : run `mongod` in a terminal.

3) In another terminal, run the MongoDB shell with the (default) name of our database : `mongo picospider`

   This initiliases our database so we can add data to it.  MongoDB should be ready to use now.  
   
4) By default, this is setup to use the `torrents` collection inside our `picospider` database. To look through any stored data from the spider in your `mongo` shell, `.find()` is your friend: 

    db.torrents.find()
    db.torrents.find().length() 
    
See http://docs.mongodb.org/manual/reference/method/db.collection.find/#db.collection.find for more on querying if needed.

Performance / Statistics 
------------------------

I've included a [text file](/past_run_stats.txt) which includes statistics dumps from test runs of the `katt`(kickass.to) spider _only_.

All test runs were done on a moderately powerful Ubuntu desktop & modest residential internet connection.

Notable information:
* Longest run scraped 36047 items in a bit over 3 hours.
* Data collection is very accurate & thorough, 100% in recent runs after some Xpath tweaks - on one test run, I did not find a single object inserted into the DB had a missing or incorrect field, out of 15998.


 







    
