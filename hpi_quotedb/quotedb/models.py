from django.db import models

# Create your models here.

class Quote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default="")

