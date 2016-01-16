from django.db import models

import hashlib
import random
import string

from hpi_quotedb.quotedb.util import get_username

# Create your models here.

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
    quote = models.ForeignKey("Quote")
    value = models.IntegerField(default=1)
    hash = models.CharField(blank=True, default="", max_length=255)

    @staticmethod
    def generate_vote_hash(quote, user):
        string = str(quote.pk) + user + VoteKey.get()
        return hashlib.md5(string.encode("utf-8")).hexdigest()

class Quote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default="")
    visible = models.BooleanField(default=False)
    voting = models.IntegerField(default=0)

    def update_votes(self):
        votes = Vote.objects.all().filter(quote=self)
        old_voting = self.voting
        self.voting = votes.filter(value=1).count() - votes.filter(value=-1).count()
        if old_voting != self.voting:
            self.save()

    def process_voted(self, request):
        hash = Vote.generate_vote_hash(self, get_username(request))
        votes = Vote.objects.all().filter(quote=self, hash=hash)
        if votes.count() == 0:
            self.voted = 0
        else:
            self.voted = votes[0].value
        return self
    
    @property
    def upvotes(self):
        return Vote.objects.filter(quote=self, value=1).count()

    @property
    def downvotes(self):
        return Vote.objects.filter(quote=self, value=-1).count()

