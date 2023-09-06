from django.http import HttpResponse

from .models import Task
from .services import Scrapper


def index(request):
    task = Task.objects.first()
    scrp = Scrapper(task=task)
    results = scrp.check_results()
    return HttpResponse(results)

