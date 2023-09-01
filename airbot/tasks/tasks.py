from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings

from airscraper.notificator.notificator.spiders.offers import OffersSpider
from tasks.models import Task


def start_scrapy(task: Task):
    args = task.__dict__
    args.pop("_state")
    args.pop("id")
    args.pop("chat_id")
    results = []

    settings = get_project_settings()
    settings["LOG_LEVEL"] = "INFO"
    process = CrawlerProcess(settings)

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    process.crawl(OffersSpider, **args)
    process.start(stop_after_crawl=True, install_signal_handlers=False)
    return results
