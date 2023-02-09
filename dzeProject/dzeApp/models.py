from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', default=None)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    group = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
