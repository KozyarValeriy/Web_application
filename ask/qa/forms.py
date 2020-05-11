from django import forms
from django.contrib.auth.models import User
from django.db import models

from .models import Question, Answer


# форма добавления вопроса
class AskForm(forms.Form):
    # поле заголовка
    title = forms.CharField(max_length=200)
    # поле текста вопроса
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user, _ = User.objects.get_or_create(username='x')
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        text = self.cleaned_data['text']
        title = self.cleaned_data['title']
        if not len(text) or not len(title):
            return forms.ValidationError('Error in form')
        super(AskForm, self).clean()

    def save(self) -> Question:
        data = {"text": self.cleaned_data["text"], "title": self.cleaned_data["title"], "author": self.user}
        question = Question(**data)
        question.save()
        return question


# форма добавления ответа
class AnswerForm(forms.Form):
    # поле текста ответа
    text = forms.CharField(widget=forms.Textarea)
    # question - поле для связи с вопросом
    question = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user, _ = User.objects.get_or_create(username='x')
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        text = self.cleaned_data['text']
        if not len(text):
            return forms.ValidationError('Error in form')
        super(AnswerForm, self).clean()

    def save(self, question):
        data = {"text": self.cleaned_data["text"], "author": self.user, "question": question}
        answer = Answer(**data)
        answer.save()
        return answer


# форма добавления вопроса
class SignUpForm(forms.Form):
    # поля для регистрации нового пользователя
    username = forms.CharField()
    email = forms.EmailField(required=False)
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        # self._user, _ = User.objects.get_or_create(username='x')
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not len(username) or not len(password):
            return forms.ValidationError('Error in form')
        try:
            User.objects.get(username=username)
            return forms.ValidationError('User already exist')
        except Exception:
            super(SignUpForm, self).clean()

    def save(self) -> User:
        data = {"username": self.cleaned_data["username"],
                "password": self.cleaned_data["password"],
                "email": self.cleaned_data["email"]}
        user = User(**data)
        user.save()
        return user

    @staticmethod
    def get_user(username: str, password: str) -> User or None:
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return user
            return None
        except Exception:
            return None
