from django.db import models

# Create your models here.
class SummaryStorage(models.Model):
    username = models.CharField(max_length = 200)
    user_summary = models.TextField()

class ListStorage(models.Model):
    username = models.CharField(max_length = 200)
    user_list = models.TextField()