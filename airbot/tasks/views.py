
from django.http import HttpResponse

from .models import Task
from .services import Scrapper, TelegramBot


def index(request):
    task = Task.objects.first()
    scrp = Scrapper(task=task)
    results, total = scrp.check_results()
    if results:
        bot = TelegramBot(task, results)
        bot.send_changes()
        return HttpResponse(content=f"total: {len(total)}")
    return HttpResponse(f"No new offers:(\ntotal: {len(total)}")
