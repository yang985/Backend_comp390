from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, models
from django.http import HttpResponse
import json
from django.contrib.auth import logout as django_logout


def getUserInfo(request):
    # if request.META.get("HTTP_COOKIE"):
    #
    #     # print(request.session,'----session')
    #     # print(request.COOKIES,'----cookie')
    if request.user.is_authenticated:
        access =''
        if request.user.is_staff:
            access='admin'
        else:
            access='user'

        response = JsonResponse({
            'data': {
                'isLogin': True,
                'access': access,
                'username': request.user.username,
                'email': request.user.email,
                'userId':request.user.id
            }
        })
        return response
    else:

        response = JsonResponse({
            'data':{
                'isLogin':False,
            },
            # 'errorCode':'401',
            # 'errorMessage':'please login in first',

            })
        return response


# @csrf_exempt
def signin(request):
    # get username and password
    js_data = json.loads(request.body)
    userName = js_data['username']
    passWord = js_data['password']
    type = js_data['type']
    user = authenticate(username=userName, password=passWord)
    if user is not None:
        if user.is_active:
            # whether is he a superuser?
            if user.is_staff:
                login(request, user)
                # save type of user in session when he is superuser
                request.session['usertype'] = 'admin'
                request.session['is_login'] = True
                request.session['user1'] = userName
                response = JsonResponse({'status':'ok','access':'admin','msg': 'user type: admin','type':type})
                return response
            else:
                login(request, user)
                request.session['usertype'] = 'user'
                request.session['is_login'] = True
                request.session['user1'] = userName
                response = JsonResponse({'status':'ok','access':'user','msg': 'user type: user','type':type})
                return response
        else:
            return JsonResponse({'status':'unknown','msg': 'this account isn\'t active','type':type})

    else:
        return JsonResponse({'status':'error','msg': 'there is a problem with username or password','type':type})


# @csrf_exempt
def logout(request):
    django_logout(request)
    request.session.flush() # 删除一条记录包括(session_key session_data expire_date)三个字段
    return JsonResponse({'msg':'bye...'})

# @csrf_exempt
from django.contrib.auth.models import User
def register(request):
    if request.method == 'POST':
        js_data = json.loads(request.body)
        same_userWithEmail = models.User.objects.filter(email = js_data['mail'])
        if same_userWithEmail:
            return JsonResponse({'status':'fault','message':'This email has already exist'})
        same_userWithUsername = models.User.objects.filter(username = js_data['username'])
        if same_userWithUsername:
            return JsonResponse({'status':'fault','message':'This username has already exist'})
        #create new user
        newUser = User.objects.create_user(js_data['username'],js_data['mail'],js_data['password'])
        newUser.is_staff = 0
        newUser.save()
        return JsonResponse({'status': 'ok','message':'successfully registered'})
    else:
        return JsonResponse({'data': 4, 'msg': 'wrong request method!'})
