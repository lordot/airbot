from django.contrib import admin
from django.forms import forms

<<<<<<< HEAD
from .models import Task, Room, Offer
=======
from .models import Task
>>>>>>> 3bec8d3025f44fe31df7c51d511cc2c2f2024e3b


class TaskForm(forms.Form):
    class Meta:
        model = Task
        fields = '__all__'


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm


admin.site.register(Task)
<<<<<<< HEAD
admin.site.register(Room)
admin.site.register(Offer)
=======
>>>>>>> 3bec8d3025f44fe31df7c51d511cc2c2f2024e3b
