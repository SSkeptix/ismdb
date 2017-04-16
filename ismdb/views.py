from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
# Create your views here.

@login_required(login_url="/account/login/")
def home(request):
	return render(request, "home.html")

def debuging(request):

	count = 33
	string = ''
	for i in range(1, int(count/10) + 2):
		string += str(i)
	return HttpResponse(string)

