from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    #return HttpResponse("Welcome to home page")
    return render(request,"home.html")
