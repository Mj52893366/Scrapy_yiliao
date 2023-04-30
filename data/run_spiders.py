from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data.spiders import a39net
from data.spiders import haodaifu
from data.spiders import xywy


def run_spiders():
    process = CrawlerProcess(get_project_settings())

    process.crawl(xywy.XywySpider)
    process.crawl(a39net.A39netSpider)
    process.crawl(haodaifu.HaodaifuSpider)

    process.start()


if __name__ == "__main__":
    run_spiders()
