from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse

def getUserInfo(request):
    return HttpResponse('user info.....')