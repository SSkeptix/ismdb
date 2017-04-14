from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
#from . import forms
#from . import tuples
#from . import models

from django.http import HttpResponse


# Create your views here.
def search(request):

	args = {}






	return render(request, 'core/search.html', args)

