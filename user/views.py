from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # 写的非常好
import simplejson  #pip install simplejson
from messages import Messages
from django.views.decorators.http import require_POST, require_GET, require_http_methods


'''
用户功能设计与实现
提供用户注册处理，
用户登录处理，
提供路由配置
'''


# Create your views here.
#所有的视图函数（view）都要有一个request进来
#用装饰器来捕获post方法
'''
自己写的
def required_methods(methods):
    def method(viewfunc):  #reg->viewfunc
        def warpper(request, *arg, **kwargs):
            if request.method.lower() == 'post':
                ret = viewfunc(request, *arg, **kwargs)  #此处的*是参数解构
                return ret
            else:
                return JsonResponse({},status=405)
        return warpper
    return method

#写reg函数  用户注册
@required_methods(['get', 'post'])
'''
@require_POST    #用系统的
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



'''
用户登录接口设计
POST /user/login 用户登录

请求体 application/json
{
  "username":"string"
  "password":"string"
}

响应：成功 200；失败 200，并返回错误信息

接收 用户通过POST方法提交的登录信息，提交的数据是JSON格式数据
{
  "username":"string"
  "password":"string"
}
从auth_user表中使用username找出匹配的一条记录，验证密码是否正确；
验证 通过说明是合法用户登录，显示欢迎页面；失败 返回错误号和描述；
整个过程都采用AJAX异步过程，用户提交JSON数据，服务端获取数据后处理，返回JSON。



'''
@require_POST
def user_login(request):   #HttpRequest
    #进入到视图函数中，request中应该有2个动态属性，session,user

    #打印request的path，GET,POST,method,body,content_type
    print(request.path)
    # print(request.GET)  #查询字符串
    # print(request.POST)  #表单提交
    print(request.method)
    print(request.body)
    print(request.content_type) #application/json
    print(request.is_ajax())

    #try:解析request.bodyjson数据成字典类型，获取用户名 except
    try:
        payload = simplejson.loads(request.body)
        print(type(payload), payload)   #dict类型
        username = payload['username'] #登录 怎么处理？ 不需在数据库中比较。先看用户名。对密码再做加密再比较
        password = payload['password']
        #认证
        user = authenticate(username = username, password = password) #认证函数，用户名和密码匹配的问题；匹配成功相当于和数据一一对应
                                                           # 返回user实例,是真实存在的用户 is_authenticated永远是True
        print(type(user), user)
        print(type(request.user), request.user)  # 目前是匿名的，匿名用户也是用户，但是is_authenticated永远是false
        print(request.session)
        #判断认证结果，用户是否为空
        if user:     #登录成功
            #cookie和session. 首先必须对认证成功者发一个身份ID，response中增加set-cookie,至少应该有sid(session id).sid必须保存在服务端
            login(request, user) #习惯上，各种后台(jsp,php)，都通过request.session获取session值。创建与当前用户相关的
                                 #login就是将user捆到request对象上
            return HttpResponse(status=204) # 用户认证成功后 该如何？
        return JsonResponse({Messages.INVALID_USERNAME_OR_PASSWORD}, status=200)  #用户为NONE时，返回的信息
    except Exception as e:   #错误的
        print(e)
        return JsonResponse({Messages.BAD_REQUEST}, status=200) #浏览器端不能如时相告；；；用户错误时返回的信息


'''
在以后业务方法中，有些业务方法要求用户登录后才可访问，如何做到：
1、@login_required装饰器
（该装饰器会在服务器端重定向。本次项目是前后段分离，需要后端返回状态值，是由前端路由实现跳转。所以此装饰器不合适）
2、中间件技术
3、自定义装饰器


@login_required装饰器
装饰器视图函数判断是否登录，如果未登录则在服务器端跳转到登录页，也可指定登录页paht。

'''
@login_required  #user_logout=login_required(user_logout)
@login_required(login_url='/users/login') #user_logout=login_required(login_url='/users/login')(user_logout)
def user_logout(request):

    return HttpResponse('looked it')





