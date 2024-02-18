from typing import Union
from fastapi import FastAPI
import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher

app = FastAPI()


@app.get("/")
def read_root():
    return get_selling_package()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class ZoneData(scrapy.Item):
    list = scrapy.Field()


class BuyvmSpider(scrapy.Spider):
    name = 'buyvm'
    start_urls = ['https://my.frantech.ca/cart.php?gid=' + str(id) for id in [37, 38, 48, 39, 42, 49, 45, 46]]

    def parse(self, response):
        zoneData = ZoneData()
        zoneData.list = []
        for div in response.css('.products .col-lg-4'):
            stock = 10000
            try:
                stock = int(re.findall(r"(\d*) Available", div.css('.package-qty::text').get())[0])
            except:
                pass
            info = {'package_name': div.css('.package-name::text').get(),
                    'price': float(re.findall(r"(\d+\.\d+) USD", div.css('.price::text').get())[0]),
                    'stock': stock}
            zoneData.list.append(info)

        yield zoneData


def get_selling_package():
    results = []
    dispatcher.connect(lambda signal, sender, item, response, spider: results.append(item), signal=signals.item_scraped)
    process = CrawlerProcess(get_project_settings())
    process.crawl(BuyvmSpider)
    process.start()
    return results

    # if __name__ == "__main__":


t = CrawlerProcess()


def item_scraped(item, response, spider):
    print("===%s", item)


# do something with the item

def test_furla():
    # we need Crawler instance to access signals
    crawler = t.create_crawler(BuyvmSpider)
    crawler.signals.connect(item_scraped, signal=signals.item_scraped)
    x = t.crawl(crawler)
    return x


test_furla()
t.start()
