pico-nova
=========

Scrapers / crawlers for 5 popular public BitTorrent sites: 

http://kickass.to, http://mininova.org, http://thepiratebay.se, http://h33t.com, & http://fenopy.se . 

Uses the Scrapy web scraping framework for Python 2.7 - http://scrapy.org/


Available Spiders
=================

The most developed spider is "katt", for http://kickass.to . It's been tuned to give very reliable data.  It is found in 

    piconova/spiders/picokatt.py

All the other spiders have a lesser degree of specialization. All of the spiders subclass the "PicoSpider" found in `piconova/spiders/picolib.py`, and pass in a dictionary of Xpaths for scraping their torrent pages.  Some override the default callbacks for parsing pages to deal with site-specific issues.  

To crawl a domain (given that the data store / MongoDB connection is setup), run this from anywhere in the repo directory:

    scrapy crawl <spider name>
    
Domain   :  Spider Name
---------------------------
kickass.to : "picokatt"

h33t.com :  "picoh33t"

thepiratebay.se : "picobay"

mininova.org : "piconova"

fenopy.se : "fenopico"


Dependencies & Installation
===========================

* Python 2.7
* Scrapy - depends on `pip`, `lxml` , `OpenSSL` ; see http://doc.scrapy.org/en/latest/intro/install.html for more on installing scrapy


Data Store Setup / Use (MongoDB)
===============================

This spider stores scraped torrent objects in a MongoDB collection.  To setup:

1) Install MongoDB for your platform of choice if not installed.  http://docs.mongodb.org/manual/installation/

2) Start a `mongod` instance for the spider to bind to : run `mongod` in a terminal.

3) In another terminal, run the MongoDB shell with the (default) name of our database : `mongo picospider`

   This initiliases our database so we can add data to it.  MongoDB should be ready to use now.  
   
4) By default, this is setup to use the `torrents` collection inside our `picospider` database. To look through any stored data from the spider in your `mongo` shell, `.find()` is your friend: 

    db.torrents.find()
    db.torrents.find().length() 
    
See http://docs.mongodb.org/manual/reference/method/db.collection.find/#db.collection.find for more on querying if needed.
 







    
