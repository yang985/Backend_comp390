from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm
from django.http import Http404, HttpResponse, HttpResponseForbidden
import json
from django.contrib.auth import logout as django_logout


# @csrf_exempt
def getUserInfo(request):
    if request.META.get("HTTP_COOKIE"):
        print('having request cookies')
        print(request.META.get("HTTP_COOKIE"))
        print(request.session,'----session')
        print(request.COOKIES,'----cookie')
    if request.user.is_authenticated:
        print(request.user)
        response = JsonResponse({
            'data': {
                'username': request.user.username,
                'email': request.user.email,
            }
        })
        # response["Access-Control-Allow-Origin"] = "http://localhost:8001"
        # response["Access-Control-Allow-Methods"] = "GET,POST"
        # response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
        return response
    else:

        response = HttpResponse(JsonResponse({
            'data':{
                'isLogin':'false',
            },
            'errorCode':'401',
            'errorMessage':'please login in first',

            }),status=403)
        # response["Access-Control-Allow-Origin"] = "http://localhost:8001"
        # response["Access-Control-Allow-Methods"] = "GET,POST"
        # response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
        return response


# @csrf_exempt
def signin(request):
    # get username and password
    js_data = json.loads(request.body)
    print(js_data)
    # password, username = request.body
    userName = js_data['username']
    passWord = js_data['password']
    type = js_data['type']
    # print(userName)
    # print(passWord)

    # authenticate by django.auth
    user = authenticate(username=userName, password=passWord)

    if user is not None:
        if user.is_active:
            # whether is he a superuser?
            if user.is_superuser:
                login(request, user)
                # save type of user in session when he is superuser
                request.session['usertype'] = 'manager'
                request.session['is_login'] = True
                request.session['user1'] = userName
                print(request.session.session_key)
                response = JsonResponse({'status':'ok','data': 1,'is_admin':1,'msg': 'user type: manager','type':type})
                # response["Access-Control-Allow-Origin"] = "http://localhost:8001"
                # response["Access-Control-Allow-Methods"] = "GET,POST"
                # response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
                return response
            else:
                login(request, user)
                request.session['usertype'] = 'user'
                request.session['is_login'] = True
                request.session['user1'] = userName
                print(request.session.session_key)
                response = JsonResponse({'status':'ok','data': 2,'is_admin':0,'msg': 'user type: user','type':type})
                # response["Access-Control-Allow-Origin"] = "http://localhost:8001"
                # response["Access-Control-Allow-Methods"] = "GET,POST"
                # response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
                return response
        else:
            return JsonResponse({'status':'unknown','data': 3, 'msg': 'this account isn\'t active','type':type})

    else:
        return JsonResponse({'status':'error', 'msg': 'there is a problem with username or password','type':type})


# @csrf_exempt
def logout(request):
    django_logout(request)
    request.session.flush() # 删除一条记录包括(session_key session_data expire_date)三个字段
    return JsonResponse({'msg':'bye...'})

# @csrf_exempt
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
                return JsonResponse({'data': 1, 'msg': message})
            else:
                # check username
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:
                    return JsonResponse({'data': 2, 'msg': 'Username already exists'})

            return JsonResponse({'data': 5, 'msg': 'form is not validate, error isn\'t defined'})

    else:
        return JsonResponse({'data': 4, 'msg': 'wrong request method!'})
