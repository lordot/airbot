from tasks.models import Task, Room, Offer


class Scrapper:

    def __init__(self, task: Task):
        self.task_id = task.__dict__.pop("id")
        self.args = task.__dict__
        self.results = self.start_scrapy()

    def start_scrapy(self):
        """
        Scrapping results from task
        """
        self.args.pop("_state")
        self.args.pop("chat_id")

        return None

    def check_results(self) -> list[Offer]:
        """
        Compare results with database
        """
        new_offers = [item["id"] for item in self.results]
        old_offers = Offer.objects.filter(task_id=self.task_id)  # TODO исправить

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

        return news

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
                    name=room["name"],
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
