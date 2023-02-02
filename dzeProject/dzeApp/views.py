import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from .forms import StudentRegistrationForm
from .models import Student


def index(request):
    dateStartJob = datetime.date(2020, 8, 26)
    days = datetime.date.today() - dateStartJob
    daysToday = days.days
    hoursInJob = int(daysToday * 2.1)
    consultHours = int(14 * 8 * 2.5)
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


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            group = form.cleaned_data.get('group')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            student = Student(user=user, first_name=first_name, last_name=last_name, group=group)
            student.save()
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'dzeApp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

