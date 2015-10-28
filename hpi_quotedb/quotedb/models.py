from django.db import models

import hashlib
import random
import string

# Create your models here.

class Quote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default="")

def random_string(length):
    return "".join([ random.choice(string.ascii_letters + string.digits) for i in range(length) ])

class VoteKey(models.Model):
    key = models.CharField(blank=True, default="", max_length=255)

    @staticmethod
    def get():
        keys = VoteKey.objects.all()
        if keys.count() == 0:
            return VoteKey.objects.create(key=random_string(16)).key
        elif keys.count() == 1:
            return keys[0].key
        else:
            # there may be only one key
            key = keys[0]
            # delete all except one
            VoteKey.objects.all().exclude(pk=key.pk)
            return key.key

class Vote(models.Model):
    quote = models.ForeignKey(Quote)
    value = models.IntegerField(default=1)
    hash = models.CharField(blank=True, default="", max_length=255)

    @staticmethod
    def generate_vote_hash(quote, user):
        string = str(quote.pk) + user + VoteKey.get()
        return hashlib.md5(string).hexdigest()

