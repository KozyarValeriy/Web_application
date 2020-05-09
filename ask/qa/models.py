# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    """ Класс менеджер для Question  """

    def new(self):
        """ Метод, возарвщающий последний новый вопрос """
        return self.ordered_by("-added_at")

    def popular(self):
        """ Метод возвращающий вопросы отсортированные по рейтингу """
        return self.ordered_by("-rating")


class Question(models.Model):
    objects = QuestionManager()
    # Добавление полей
    title = models.CharField(max_length=200)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='question_like_user')


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
