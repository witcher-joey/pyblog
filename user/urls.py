from django.urls import path
from .views import reg, user_login, user_logout

#此处的路由对应user（子应用）的views(user子应用的视图函数)
urlpatterns=[
    path('',reg), # reg psot  匹配user中视图函数
    path('login', user_login),   #post /user/login  登录函数路由
    path('logout', user_logout)
]