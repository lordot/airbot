import requests

from django.conf import settings

from tasks.models import Task, Room, Offer


class Scrapper:

    def __init__(self, task: Task):
        self.args = task.__dict__.copy()
        self.args.pop("_state")
        self.task_id = self.args.pop("id")
        self.chat_id = self.args.pop("chat_id")
        self.results = self.start_scrapy()

    def start_scrapy(self):
        """
        Scrapping results from task
        """
        response = requests.post(f"http://{settings.AIRSCRAPER_HOST}:8000",
                                 json=self.args)  # TODO переделать под переменную сервера или нет
        data = response.json()  # TODO если больше 360 то рейсить ошибку и не сравнивать
        return data

    def check_results(self) -> tuple[list[Offer], dict]:
        """
        Compare results with database
        """
        total = self.results.copy()
        new_offers = [item["id"] for item in self.results]
        old_offers = Offer.objects.filter(task_id=self.task_id)

        del_offers = []
        for offer in old_offers:
            if offer.room_id in new_offers:
                for item in self.results:
                    if item["id"] == offer.room_id and self.task_id == offer.task_id:
                        self.results.remove(item)
            else:
                del_offers.append(offer)

        self.create_rooms(self.results)
        deleted = self.delete_offers(del_offers)
        news = self.create_offers(self.results)

        return news, total

    @staticmethod
    def create_rooms(results: list):
        """
        Create room if needed
        """
        new_rooms = []
        exists = list(Room.objects.values_list("id", flat=True))
        for room in results:
            if room["id"] not in exists:
                new = Room(
                    id=room["id"],
                    name=room["name"].translate({ord(i): None for i in "'()._*~,>+#[]|!{}=-"}),
                    type=room["type"],
                    rate=room.get("rate", None),
                    reviews=room.get("reviews", None)
                )
                new_rooms.append(new)
        Room.objects.bulk_create(new_rooms)

    def create_offers(self, results: list) -> list[Offer]:
        """
        Create offers and return them
        """
        new_offers = []
        for offer in results:
            new_offer = Offer(
                room_id=offer["id"],
                task_id=self.task_id,  # TODO исправить
                price=offer.get("price", None),
                checkin=offer["checkin"],
                checkout=offer["checkout"]
            )
            new_offers.append(new_offer)
        new_offers = Offer.objects.bulk_create(new_offers)
        return new_offers

    @staticmethod
    def delete_offers(offers: list[Offer]) -> list[Offer]:
        """
        Delete offers and return it
        """
        ids = [offer.id for offer in offers]
        queryset = Offer.objects.filter(id__in=ids)
        queryset._raw_delete(queryset.db)
        return offers


class TelegramBot:
    def __init__(self, task: Task, new_offers: list[Offer]):
        self.task = task
        self.new_offers = new_offers
        self.api_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        self.offer_url = "https://ru.airbnb.com/rooms/"

    def send_changes(self) -> dict:
        response = requests.post(
            url="https://api.telegram.org/bot{0}/sendMessage".format(settings.BOT_TOKEN),
            data={"chat_id": self.task.chat_id, "parse_mode": "MarkdownV2", "text": self._message()}
        ).json()
        print(response)
        return response

    def _message(self) -> str:
        message = f"*Query: {self.task.id}: {self.task.query} {self.task.price_min} - {self.task.price_max}:*\n\n"

        for offer in self.new_offers:
            message += f" - [{offer.room.name.capitalize()}]({self.offer_url + str(offer.room.id)}) {offer.checkin} - {offer.checkout} - *{offer.price}*\n"

        message = message.replace("-", "\\-")
        return message
