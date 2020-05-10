# Контроллер для приложения qa

from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Model

from .models import Question, Answer


def test(request: HttpRequest, *args, **kwargs):
	print(args)
	print(kwargs)
	response = HttpResponse(content="OK")
	return response


def get_page(request: HttpRequest):
	""" Функция для обработки url: /?page=... """
	# получаем вопросы, отсортированнаые по убыванию по id
	question = Question.objects.new()
	# получаем список вопросов на текущую страницу
	page = get_paginator_page(request, question, limit=10)
	content = {"page": page}
	return render(request, "qa/index.html", content)


def get_popular(request: HttpRequest):
	""" Функция для обработки url: popular/?page=... """
	# получаем вопросы, отсортированнаые по убыванию по rating
	question = Question.objects.popular()
	# получаем список вопросов на текущую страницу
	page = get_paginator_page(request, question, limit=10)
	content = {"page": page}
	return render(request, "qa/index.html", content)


def get_question(request: HttpRequest, question_id: int):
	""" Функция для обработки url: question/<int:question_id>/ """
	# получаем вопрос с указанным id
	question = get_object_or_404(Question, id=question_id)
	# получаем все ответы на данный вопрос
	answers = Answer.objects.filter(question_id=question.id)
	content = {"question": question, "answers": answers}
	return render(request, "qa/question_page.html", content)


def get_paginator_page(request: HttpRequest, obj: Model, limit=10):
	""" Функция для получения пагинатора для входного объекта
		для url: ...?page=...
	"""
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		raise Http404
	paginator = Paginator(obj, limit)
	try:
		page = paginator.page(page)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return page
