from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm


@csrf_exempt
def getUserInfo(request):
    return HttpResponse('user info.....')


@csrf_exempt
def signin(request):
    # get username and password
    userName = request.POST.get('username')
    passWord = request.POST.get('password')
    print(userName, passWord)

    # authenticate by django.auth
    user = authenticate(username=userName, password=passWord)

    if user is not None:
        if user.is_active:
            # whether is he a superuser?
            if user.is_superuser:
                login(request, user)
                # save type of user in session when he is superuser
                request.session['usertype'] = 'manager'
                return JsonResponse({'data': 1, 'msg': 'user type: manager'})
            else:
                login(request, user)
                request.session['usertype'] = 'user'
                return JsonResponse({'data': 2, 'msg': 'user type: user'})
        else:
            return JsonResponse({'data': 3, 'msg': 'this account isn\'t active'})

    else:
        return JsonResponse({'data': 0, 'msg': 'there is a problem with username or password'})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():  # django self-checking

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            # check section for new attributes(email,first_name....)
            # check email
            same_email_user = models.User.objects.filter(email=email)
            if same_email_user:
                return JsonResponse({'data': 3, 'msg': 'This email has already registered'})

            # save user in db
            form.save()
            # new_user = models.User()
            # new_user.last_name = last_name
            # new_user.first_name = first_name
            # new_user.password = password1
            # new_user.email= email
            # new_user.username =username
            # new_user.save()
            return JsonResponse({'data': 0, 'msg': 'welcome!!!'})

        else:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # check passwords
            if password1 != password2:
                message = 'Passwords are different!'
                return JsonResponse({'data': 1, 'msg': 'passwords are different'})
            else:
                # check username
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:
                    return JsonResponse({'data': 2, 'msg': 'Username already exists'})

            return JsonResponse({'data': 5, 'msg': 'form is not validate, error isn\'t defined'})

    else:
        return JsonResponse({'data': 4, 'msg': 'wrong request method!'})
