from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import models


from django.http import HttpResponse






def test(request):
	return render(request, 'core/test.html')