"""
Dev: f97gp1@gmail.com

This file fecth "New Popular Movies from Yts web page".
If a new set of Pupular Moovies will appear then, will be
send it a email. 

This script use the boto3 library & the SES client from
Amazon Web Services.

The next updates will used the smtplib from the python
core libraries.

Add manually intto the crontab

> sudo nano /etc/crontab
(select how many often do you want to run the script)
(put the complete route before the execution)

Example  of the add:
    * 10 * * 7  cd 'abssolute_route' && python3 yts_notifier.py
"""

import os
import scrapy
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
from sqlclient import dbMaker
from time import gmtime, strftime
from ses_template import TemplateSender

DBNAME = "NewMovies.db"

class YtsNotifier(Spider):

    name = "NewYtsMovies"
    
    def start_requests(self):
        yield scrapy.Request("https://yts.am/", callback=self.getPosters)


    def getPosters(self, response):
        # links extractor
        item = response.xpath('//*[@id="popular-downloads"]/div[2]/div/a/@href').extract() 
        N = len(item)
        if N > 0:
            # img extractor
            ref = response.url[:-1]
            imgs = response.xpath('//*[@id="popular-downloads"]/div[2]/div/a/figure/img/@src').extract()
            poster = list(map(lambda x: ref + x, imgs))

            dbUpdate = dbMaker(name=DBNAME, table_name="Movies")
            dbUpdate.connect()
            dbUpdate.makeCursor()

            self.TemplateData = []

            for i in range(N):
                Pass = dbUpdate.insertion(
                "\"{}\", \"{}\"".format(
                                    strftime("%Y-%m-%d", gmtime()),
                                    item[i]
                                )
                )
                if Pass == True:
                    self.TemplateData.append(
                        {
                            "Url": item[i],
                            "Image": poster[i]
                        }
                    )
            dbUpdate.close()

            # Sending notifications
            if len(self.TemplateData) > 0:
                sender = TemplateSender(
                                templateData={
                                    "item"  : self.TemplateData
                                }
                                
                        )
                sender.fill_atrs(fileroute="ses_atributes.json")
                sender.start_client()
                # sender.update_template()
                sender.send_template()

if __name__ == '__main__':

    if DBNAME not in os.listdir():
        # Create the database
        db = dbMaker(name=DBNAME)
        db.connect()
        db.makeCursor()
        db.executeLine(
            """CREATE TABLE Movies (
                Date TEXT NOT NULL,
                Url TEXT NOT NULL,
                PRIMARY KEY(Date, Url)
            )"""
        )
        db.commit()
        db.close()
        print("Database {} created.".format(DBNAME))

    # POSTING a valid USER-AGENT
    process = CrawlerProcess({
                'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
				"Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
				'HTTPPROXY_ENABLED': 'True',
				'CONCURRENT_REQUESTS': 1,
				'DNS_TIMEOUT': 10,
				'DOWNLOAD_TIMEOUT' : 120
            })

    process.crawl(YtsNotifier())
    process.start()
