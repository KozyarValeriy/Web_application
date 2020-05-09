# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class QuestionManager(models.Manager):
    """ Класс менеджер для Question  """

    def new(self):
        """ Метод, возарвщающий последний новый вопрос """
        return self.order_by("-id")

    def popular(self):
        """ Метод возвращающий вопросы отсортированные по рейтингу """
        return self.order_by("-rating")


# Question - вопрос
class Question(models.Model):
    objects = QuestionManager()
    # Добавление полей
    # title - заголовок вопроса
    title = models.CharField(max_length=200)
    # text - полный текст вопроса
    text = models.TextField()
    # added_at - дата добавления вопроса
    added_at = models.DateTimeField(auto_now_add=True)
    # rating - рейтинг вопроса (число)
    rating = models.IntegerField(default=0)
    # author - автор вопроса
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes - список пользователей, поставивших "лайк"
    likes = models.ManyToManyField(User, related_name='question_like_user')

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('qa:question', args=(self.id, ))


# Answer - ответ
class Answer(models.Model):
    # text - текст ответа
    text = models.TextField()
    # added_at - дата добавления ответа
    added_at = models.DateTimeField(auto_now_add=True)
    # question - вопрос, к которому относится ответ
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # author - автор ответа
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
