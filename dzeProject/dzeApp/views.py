import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


from .models import Student



def index(request):
    dateStartJob = datetime.date(2020, 8, 26)
    days = datetime.date.today() - dateStartJob
    daysToday = days.days
    hoursInJob = int(daysToday * 2.1)
    consultHours = int(14 * 8 * 2.5)
    context = {'daysToday': daysToday, 'hoursInJob': hoursInJob, 'consultHours': consultHours,
               'is_authenticated': request.user.is_authenticated}

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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        group = request.POST.get('group')
        username = request.POST.get('usernameReg')
        password = request.POST.get('password1')
        user = User.objects.create_user(username=username, password=password)
        student = Student(user=user, first_name=first_name, last_name=last_name, group=group)
        student.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('usernameLog')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid login credentials'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def send_comment(request):
    if request.method == 'POST':
        username = request.user.username
        student = Student.objects.get(user__username=username)
        message = request.POST['message-text']
        subject = 'Комментарий на проверку'
        name = f'{student.first_name} {student.last_name}'
        group = student.group
        photo = request.FILES.get('photo')
        if photo:
            email = EmailMessage(
                subject, f'{message}\n Письмо от {name}\n Группа: {group}',
                settings.EMAIL_HOST_USER, ['nikita10672@mail.ru']
            )
            email.attach(photo.name, photo.read(), photo.content_type)
            email.send()
            return redirect('success')
        else:
            try:
                send_mail(subject, f'{message}\n Письмо от {name}\n Группа: {group}',
                          settings.EMAIL_HOST_USER,
                          ['nikita10672@mail.ru'], fail_silently=False)
                return redirect('success')
            except Exception as e:
                return HttpResponse(f"Error: {e}")
