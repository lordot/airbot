from django.db import models

ROOM_TYPES = [("Entire home/apt", "entire"), ("Private room", "room")]
PICKER_TYPE = [
    ("flexible_dates", "flexible"),
    ("monthly_stay", "monthly"),
    ("calendar", "calendar")
]
TRIP_LENGTHS = [
    ("one_month,", "months"),
    ("one_week,", "weeks"),
    ("weekend_trip,", "weekend")
]


class Room(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    rate = models.FloatField(null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)


class Task(models.Model):
    chat_id = models.IntegerField()
    updated = models.BooleanField(default=False)
    rooms = models.ManyToManyField(Room, through="Offer")

    query = models.CharField(max_length=100)  # city
    price_min = models.PositiveIntegerField()
    price_max = models.PositiveIntegerField()
    room_types = models.CharField(max_length=100, choices=ROOM_TYPES)
    min_bedrooms = models.PositiveIntegerField()
    min_beds = models.PositiveIntegerField()
    date_picker_type = models.CharField(max_length=100, choices=PICKER_TYPE)

    monthly_start_date = models.DateField(null=True, blank=True)
    monthly_length = models.IntegerField(null=True, blank=True)

    checkin = models.DateField(null=True, blank=True)
    checkout = models.DateField(null=True, blank=True)

    flexible_trip_lengths = models.CharField(
        max_length=100, choices=TRIP_LENGTHS, null=True, blank=True
    )
    flexible_trip_dates = models.TextField(null=True, blank=True)
    # TODO: переделать под нормальный тип с мультивыбором

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return str(self.id)


class Offer(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    price = models.CharField(max_length=10)
    checkin = models.DateField()
    checkout = models.DateField()

    class Meta:
        unique_together = ["room", "task"]
        verbose_name_plural = "Offers"
