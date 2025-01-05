from django.db import models
import datetime
from django.utils import timezone


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = (
        ('radio', 'Single Choice'),
        ('checkbox', 'Multiple Choice'),
        ('text', 'Text Answer'),
    )
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.CharField(max_length=200)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
