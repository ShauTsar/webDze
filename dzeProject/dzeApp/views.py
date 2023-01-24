from django.shortcuts import render
import datetime

from django.http import HttpResponse


def index(request):
    dateStartJob = datetime.date(2020, 8, 26)
    days = datetime.date.today()-dateStartJob
    daysToday = days.days
    context = {'daysToday': daysToday}
    return render(request, 'dzeApp/index.html', context)
