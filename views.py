from django.http import HttpResponse
from django.shortcuts import render

#method view home
def home(request):
    return render(request, 'homepage.html')

def booking(request):
    return render(request, 'booking.html')

def index(request):
    return HttpResponse("Hello world")