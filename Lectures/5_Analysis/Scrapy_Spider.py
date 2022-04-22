import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
import csv


class RegSpider(scrapy.Spider):
    name = 'reg_crawl'
    start_urls = ["https://www.naab-css.org/dairy-cross-reference/"+str(x) \
                    for x in pd.read_csv("C:/Users/jhtchns2/work/projects/dairy_matching/code/data_collection/remaining_ids.csv")["0"]]
    custom_settings = {
                        'CONCURRENT_REQUESTS': 35,
                        'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
                        'CONCURRENT_REQUESTS_PER_IP': 50,
                        'AUTOTHROTTLE_ENABLED' : True,
                        'AUTOTHROTTLE_START_DELAY' : 1,
                        'AUTOTHROTTLE_MAX_DELAY' : 5
                      }
    def parse(self, response):
        try:
            table = response.css(".DairyCrossTable")
            table_data = table.extract()[0]
            df = pd.read_html(table_data)[0].set_index(0).T
            df['reg_id'] = response.url.split("/")[-1]
            df.to_csv("C:/Users/jhtchns2/work/projects/dairy_matching/code/data_collection/NAAB_info_data.csv",mode='a',header=None,index=False)
        except:
            id_ = response.url.split("naab=")[1]
            with open(r'C:/Users/jhtchns2/work/projects/dairy_matching/code/data_collection/sires_with_no_data.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow([id_])
               
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})
process.crawl(RegSpider)
process.start()