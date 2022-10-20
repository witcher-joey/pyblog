from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
import simplejson  #pip install simplejson
from messages import Messages


# Create your views here.

#写reg函数  用户注册
def reg(request:HttpRequest):
    #测试代码  这些都是要关注的
    print('=========================')
    print('request_path:',request.path)
    print('request_get:',request.GET)  #查询字典
    print('request_post:',request.POST)
    print('request_method:',request.method)
    print('request_content:',request.content_type)
    print('==========================')
    try:          #如果没有数据， 所以要try一下
        payload=simplejson.loads(request.body)   #数据提取：将请求体解析为json数据
        print(type(payload),payload)             #打印解析后的数据（请求体）为字典型
        #获取请求体中的username\email\password
        username=payload['username']
        email=payload['email']
        password=payload['password']

        print(username,email,password)

        #永远不要相信客户端发来的数据; 判断用户是否存在
        count=User.objects.filter(username=username).count()  #得到用户数, username为唯一键
        if count>0:                               #说明用户已存在
            return JsonResponse(Messages.USER_EXISTS)         #报告信息
        #数据存储 创建新用户（注册）
        #user=User()     #新增用户你知道ID吗？不知道，  所以不需要提供id
        #user.username=username
        user=User.objects.create_user(username,email,password)  #依次看源码
        print(type(user),user)  #   一旦创建成功，看到的是User的实例


        #return HttpResponse(status=201)    #正确信息      问题：为什么正确返回的是http 请求
        return JsonResponse({},status=201)
        #return HttpResponse(content_type='application/json',status=201)
    except Exception as e:                #返回错误处理  ；错误码应该是固定好的
        return JsonResponse(Messages.BAD_REQUEST,status=200)

