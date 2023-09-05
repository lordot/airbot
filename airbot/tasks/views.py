<<<<<<< HEAD
from django.http import HttpResponse

from .models import Task
from .services import Scrapper


def index(request):
    task = Task.objects.first()
    scrp = Scrapper(task=task)
    results = scrp.check_results()
    return HttpResponse(results)
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 3bec8d3025f44fe31df7c51d511cc2c2f2024e3b
