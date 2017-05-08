from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from core.functions import validation_permission


def e404(request, msg = None):
	args = {'msg': msg, }
	return render(request, "404.html", args)


def home(request):
	args = {'validation_permission': validation_permission(user=request.user), }
	return render(request, "home.html", args)

def debuging(request):

	count = 33
	string = ''
	for i in range(1, int(count/10) + 2):
		string += str(i)
	return HttpResponse(string)

