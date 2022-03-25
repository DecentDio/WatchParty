from django.db import models
from django.contrib.auth.models import User

class Watchparty(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    title_text = models.CharField(max_length=200)
    start_date = models.DateField('date range start')
    end_date = models.DateField('date range end')
    def __str__(self):
        return self.title_text

class AvailabilityRange(models.Model):
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False)