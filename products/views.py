from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json
from products.models import Products
from django.forms.models import model_to_dict
# Create your views here.

def getProductById(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            jsonData = json.loads(request.body)
            id = jsonData['key']
            product = model_to_dict(Products.objects.get(id=id))
            return JsonResponse({'msg':'successfully','content':product,'status':'ok'})
        else:
            return JsonResponse({'msg': 'failed','status':'failed'})
    return JsonResponse({'msg':'failed','status':'failed'})


def createNewProduct(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        ownerId = jsonData['userId']
        owner = jsonData['owner']
        title =jsonData['title']
        hints =jsonData['hints']
        desc = jsonData['desc']
        label = jsonData['label']
        componentData = jsonData['componentData']
        newProduct = Products(ownerId=ownerId,owner=owner,componentData=componentData,title=title,hints=hints,desc=desc,label=label)
        newProduct.save()
        return JsonResponse({'msg':'successfully created','status':'ok'})


    return JsonResponse({'msg':'failed','status':'failed'})


def getAllProducts(request):
    if(request.method == 'POST'):
        productList = serializers.serialize('json', Products.objects.all())
        return JsonResponse({'content':json.loads(productList),'msg':'success','status':'ok'})
    return JsonResponse({'status':'failed','msg':'failed to load projects'})
