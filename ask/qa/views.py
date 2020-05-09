# Контроллер для приложения qa

from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404

from .models import Question, Answer


def test(request, *args, **kwargs):
	print(args)
	print(kwargs)
	response = HttpResponse(content="OK")
	return response


def get_page(request):
	question = Question.objects.new()
	page = get_paginator_page(request, question, limit=10)
	content = {"page": page}
	return render(request, "qa/index.html", content)


def get_popular(request):
	question = Question.objects.popular()
	page = get_paginator_page(request, question, limit=10)
	content = {"page": page}
	return render(request, "qa/index.html", content)


def get_question(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	answers = Answer.objects.filter(question_id=question.id)
	content = {"question": question, "answers": answers}
	return render(request, "qa/question_page.html", content)


def get_paginator_page(request, obj, limit=10):
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
