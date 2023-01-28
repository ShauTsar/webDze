import datetime
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
import asyncio
from django.views.decorators.csrf import csrf_exempt


def index(request):
    dateStartJob = datetime.date(2020, 8, 26)
    days = datetime.date.today() - dateStartJob
    daysToday = days.days
    hoursInJob = int(daysToday * 2.1)
    consultHours = int(14*8*2.5)
    context = {'daysToday': daysToday, 'hoursInJob': hoursInJob, 'consultHours': consultHours}

    return render(request, 'dzeApp/index.html', context)


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        message = request.POST['message']
        subject = request.POST['subject']
        email = request.POST['email']
        name = request.POST['name']
        attach = request.FILES.get('attach')
        if attach:
            email = EmailMessage(
                subject, f'{message}\n Письмо от {name}\n Почта отправителя {email}',
                settings.EMAIL_HOST_USER, ['levanidzeanna@gmail.com'],
                [email],
                headers={'Reply-To': email}
            )
            email.attach(attach.name, attach.read(), attach.content_type)
            email.send()
            return redirect('success')
        else:
            try:
                send_mail(subject, f'{message}\n Письмо от {name}\n Почта отправителя {email}',
                          settings.EMAIL_HOST_USER,
                          ['levanidzeanna@gmail.com'], fail_silently=False)
                return redirect('success')
            except Exception as e:
                return HttpResponse(f"Error: {e}")


def success(request):
    return render(request, 'dzeApp/success.html')
