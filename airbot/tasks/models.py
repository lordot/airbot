from django.db import models

ROOM_TYPES = [("Entire home/apt", "entire"), ("Private room", "room")]
PICKER_TYPE = [
    ("flexible_dates", "flexible"),
    ("monthly_stay", "monthly"),
    ("calendar", "calendar")
]
TRIP_LENGTHS = [
    ("one_month", "months"),
    ("one_week", "weeks"),
    ("weekend_trip", "weekend")
]
DATE_FORMAT = ['%d-%m-%Y']


class Task(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"!!!!!!!!!!!{self.scrapy_args()}!!!!!!!!!!!!!!!")

    chat_id = models.IntegerField()

    city = models.CharField(max_length=100)
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

    def scrapy_args(self):
        main = (
            f" -a query='{self.city}'"
            f" -a price_min={self.price_min}"
            f" -a price_max={self.price_max}"
            f" -a room_types='{self.room_types}'"
            f" -a min_bedrooms={self.min_bedrooms}"
            f" -a min_beds={self.min_beds}"
            f" -a date_picker_type={self.date_picker_type}"
            )
        if self.date_picker_type == "flexible_dates":
            main += f" -a flexible_trip_lengths={self.flexible_trip_lengths}"
            main += f" -a flexible_trip_dates='{self.flexible_trip_dates}'"

        elif self.date_picker_type == "monthly_stay":
            main += f" -a monthly_start_date={self.monthly_start_date}"
            main += f" -a monthly_length={self.monthly_length}"

        elif self.date_picker_type == "calendar":
            main += f" -a checkin={self.checkin}"
            main += f" -a checkout={self.checkout}"

        return main
