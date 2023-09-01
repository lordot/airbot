from django.http import HttpResponse

from .models import Task
from .tasks import start_scrapy


def index(request):
    tasks = Task.objects.all()
    results = start_scrapy(tasks[0])
    return HttpResponse(results)
