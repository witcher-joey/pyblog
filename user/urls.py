from django.urls import path
from .views import reg

urlpatterns=[
    path('',reg) # reg psot  匹配user中视图函数
]