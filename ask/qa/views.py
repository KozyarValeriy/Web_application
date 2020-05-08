# Контроллер для приложения qa

from django.http import HttpResponse


def test(request, *args, **kwargs):
	print(args)
	print(kwargs)
	response = HttpResponse(content="OK")
	return response
