import json
import re
import urllib.parse
from typing import Generator

import scrapy
from scrapy import Field
from scrapy import Request, Spider
from scrapy.http import Response


class RoomItem(scrapy.Item):
    id = Field(serializer=int)
    name = Field()
    type = Field()
    rate = Field(serializer=float)
    reviews = Field(serializer=int)
    price = Field()
    checkin = Field()
    checkout = Field()


class OffersSpider(Spider):
    """
    Each argument demands "-a" before:

    query="Tbilisi, Georgia"

    price_min=200
    room_types="Entire home/apt", or "Private room",
                                    (comma is needed at the end of the line)
    min_bedrooms=2
    min_beds=1
    date_picker_type=flexible_dates or monthly_stay or calendar

    if "monthly_stay":
    monthly_start_date=2023-09-04
    monthly_length=4

    if "calendar":
    checkin=2023-09-04
    checkout=2023-09-10

    # if "flexible_dates":
    # flexible_trip_dates=september, october,
                                    (comma is needed at the end of the line)
    # flexible_trip_lengths=one_month or one_week or weekend_trip,
                                    (comma is needed at the end of the line)
    """
    name = "offers"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if kwargs.get("query"):
        self.start_urls = [self.__full(kwargs)]

    def parse(self, response: Response):
        self.logger.info(response.url)
        script: str = response.css("script#data-deferred-state::text").get()
        data: dict = json.loads(script).get(
            "niobeMinimalClientData"
        )[0][1].get("data")
        result: list = (
            data["presentation"]["explore"]["sections"]
            ["sectionIndependentData"]["staysSearch"]["searchResults"]
        )

        gen_pagination: Generator = self.__gen_dict_extract("nextPageCursor",
                                                            data)
        next_page: str = next(gen_pagination)
        if next_page:
            url: str = self.start_urls[0] + f"&cursor={next_page}"
            request: Request = response.follow(url, callback=self.parse)
            yield request

        item = RoomItem()
        for room in result:
            item.clear()

            listening = room.get("listing")
            if listening:
                item["id"] = int(listening.get("id"))
                item["name"] = listening.get("name", None)
                item["type"] = listening.get("roomTypeCategory")
                try:
                    match = re.match(r"^(.*) \((.*)\)",
                                     listening.get("avgRatingLocalized"))
                    item["rate"] = float(match.group(1))
                    item["reviews"] = int(match.group(2))
                except (TypeError, AttributeError):
                    pass
            else:
                continue

            params = room.get("listingParamOverrides")
            if params:
                item["checkin"] = params.get("checkin")
                item["checkout"] = params.get("checkout")

            for key in ["discountedPrice", "originalPrice", "price"]:
                try:
                    gen_price = self.__gen_dict_extract(key, room)
                    price = next(gen_price)
                    while not price:
                        price = next(gen_price)
                    item["price"] = price
                    break
                except StopIteration:
                    continue
            yield item

    def __gen_dict_extract(self, key: str, var: dict):  # TODO а оно нужно?
        if hasattr(var, 'items'):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.__gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.__gen_dict_extract(key, d):
                            yield result

    def __full(self, kwargs):
        kwargs = self.__transform_dictionary(kwargs)
        init = "https://airbnb.com/s/any/homes?"
        params = urllib.parse.urlencode(kwargs, doseq=True)
        print(init + params)
        return init + params

    def __transform_dictionary(self, input_dict):
        transform = {}

        for key, value in input_dict.items():
            if key == 'query':
                transform[key] = str(value)
            elif value is None:
                continue
            elif ',' in str(value):
                items = [item.strip() for item in value.split(',') if
                         item.strip() != '']
                transform[key + '[]'] = [str(item) for item in items] if len(
                    items) > 1 else str(items[0])
            else:
                transform[key] = str(value)

        return transform
