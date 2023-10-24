from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=12, primary_key=True)
    password = models.CharField(max_length=12)
