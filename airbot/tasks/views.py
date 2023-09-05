from django.http import HttpResponse

from .models import Task
from .tasks import Scrapper


def index(request):
    task = Task.objects.first()
    scrp = Scrapper(task=task)
    results = scrp.check_results()
    return HttpResponse(results)
