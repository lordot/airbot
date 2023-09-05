BOT_NAME = "notificator"

LOG_LEVEL = "INFO"

SPIDER_MODULES = ["notificator.spiders"]
NEWSPIDER_MODULE = "notificator.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
