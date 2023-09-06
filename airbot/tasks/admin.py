from django.contrib import admin
from django.forms import forms

from .models import Task, Room, Offer


class TaskForm(forms.Form):
    class Meta:
        model = Task
        fields = '__all__'


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm


admin.site.register(Task)
admin.site.register(Room)
admin.site.register(Offer)

