from django import forms
from django.contrib.auth.models import User

from .models import Question, Answer


# форма добавления вопроса
class AskForm(forms.Form):
    # поле заголовка
    title = forms.CharField(max_length=200)
    # поле текста вопроса
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self._user, _ = User.objects.get_or_create(username='x')
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        text = self.cleaned_data['text']
        title = self.cleaned_data['title']
        if not len(text) or not len(title):
            return forms.ValidationError('Error in form')
        super(AskForm, self).clean()

    def save(self) -> Question:
        question = Question(**self.cleaned_data, author=self._user)
        question.save()
        return question


# форма добавления ответа
class AnswerForm(forms.Form):
    # поле текста ответа
    text = forms.CharField(widget=forms.Textarea)
    # question - поле для связи с вопросом
    question = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self._user, _ = User.objects.get_or_create(username='x')
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        text = self.cleaned_data['text']
        if not len(text):
             return forms.ValidationError('Error in form')
        super(AnswerForm, self).clean()

    def save(self, question):
        data = {"text": self.cleaned_data["text"], "author": self._user, "question": question}
        answer = Answer(**data)
        answer.save()
        return answer
