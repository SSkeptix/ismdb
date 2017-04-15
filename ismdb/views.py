from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
# Create your views here.

@login_required(login_url="/account/login/")
def home(request):
	return render(request, "home.html")

def debuging(request):

	var = '1,2,3,4,5'
	z = 3
	if str(z) in var:
		r = 'True'
	else:
		r = 'False'

	return HttpResponse('result = {0}'.format(r))