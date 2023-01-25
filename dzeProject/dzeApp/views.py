import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import  settings




def index(request):
    dateStartJob = datetime.date(2020, 8, 26)
    days = datetime.date.today()-dateStartJob
    daysToday = days.days
    context = {'daysToday': daysToday}

    return render(request, 'dzeApp/index.html', context)

def send_email(request):
    if request.method == 'POST':
        message = request.POST['message']
        subject = request.POST['subject']
        email = request.POST['email']
        name = request.POST['name']

        try:
            send_mail(subject, f'{message}\n Письмо от {name}\n Почта отправителя {email}', settings.EMAIL_HOST_USER, ['levanidzeanna@gmail.com'], fail_silently=False)
            return redirect('success')
        except Exception as e:
            return HttpResponse(f"Error: {e}")
def success(request):
    return render(request, 'dzeApp/success.html')




# def send_email(request):
#     if request.method == 'POST':
#         message = request.POST['message']
#         subject = request.POST['subject']
#         email = request.POST['email']
#
#         send_mail(subject, message + "\n Письмо от:" + email, settings.EMAIL_HOST_USER, ['nikita10672@mail.ru'], fail_silently=False)
#
#     return render(request, 'dzeApp/index.html')




