# Контроллер для приложения qa

from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Model
from django.contrib import auth
from django.urls import reverse

from .models import Question, Answer
from .forms import AskForm, AnswerForm, SignUpForm


def test(request: HttpRequest, *args, **kwargs):
	print(args)
	print(kwargs)
	response = HttpResponse(content="OK")
	return response


def login(request: HttpRequest):
	user = request.user
	print(user, user.is_authenticated())
	print(request.COOKIES)
	if request.method == "POST":
		form = SignUpForm(request.POST)
		try:
			if form.is_valid():
				username = request.POST['username']
				password = request.POST['password']
				user = SignUpForm.get_user(username=username, password=password)
				if user is not None:
					auth.logout(request)
					auth.login(request, user)
				return HttpResponseRedirect(reverse('qa:home'))
		except Exception:
			form = SignUpForm()
	else:
		form = SignUpForm()
	content = {"form": form, "path": "login"}
	return render(request, "qa/login_form.html", content)


def signup(request: HttpRequest):
	""" Функция для обработки url: /signup/ """
	user = request.user
	print(user, user.is_authenticated())
	print(request.COOKIES)
	if request.method == "POST":
		form = SignUpForm(request.POST)
		try:
			if form.is_valid():
				user = form.save()
				auth.login(request, user)
				return HttpResponseRedirect(reverse('qa:home'))
		except Exception:
			form = SignUpForm()
	else:
		form = SignUpForm()
	content = {"form": form, "path": "signup"}
	return render(request, "qa/login_form.html", content)


def get_ask(request: HttpRequest):
	""" Функция для обработки url: /ask/?page=... """
	if request.method == "POST":
		form = AskForm(request.POST)
		if form.is_valid():
			form.user = request.user
			question = form.save()
			return HttpResponseRedirect(question.get_url())
	else:
		form = AskForm()
	content = {"form": form}
	return render(request, "qa/ask_form.html", content)


def get_page(request: HttpRequest):
	""" Функция для обработки url: /?page=... """

	user = request.user
	print(user, user.is_authenticated())
	print(request.COOKIES)

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
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			form.user = request.user
			form.save(question)
		# return HttpResponseRedirect(reverse('qa:question', args=(question_id, )))
	else:
		form = AnswerForm(initial={'question': question_id})
	# получаем все ответы на данный вопрос
	answers = Answer.objects.filter(question_id=question.id)
	content = {"question": question, "answers": answers, "form": form}
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
