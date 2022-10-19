from django.shortcuts import render, HttpResponse
from django.http import HttpRequest, JsonResponse
import simplejson



# Create your views here.

#写reg函数
def reg(request:HttpRequest):
    print(request.path)
    print(request.GET)
    print(request.POST)
    print(request.method)
    print(request.content_type)
    try:          #如果没有数据， 所以要try一下
        payload=simplejson.loads(request.body)
        print(type(payload),payload)
        username=payload['username']



        return HttpResponse(status=201)
    except Exception as e:
        return JsonResponse({
            "code":"10078",
            "msh":"出错了"
        },status=200)

