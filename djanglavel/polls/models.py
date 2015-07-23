import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Simple question for a poll
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def was_published_recently(self):
        """Return true if published less than 1 day ago
        """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
