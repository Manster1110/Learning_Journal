from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """A learning entry that a learner wants to track"""
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """What was learned about each topic that is added"""
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return the string of the model being represented"""
        return self.text[:50] + "..."