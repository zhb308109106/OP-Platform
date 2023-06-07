from django.shortcuts import render

# Create your views here.
from django.contrib import auth

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
import random
@permission_classes((AllowAny,))
@authentication_classes(())
class AuthView(APIView):
  def post(self,request):
    """登录"""
    result = True
    errorInfo = ''
    detail = {}
    username = request.data.get('name')
    password = request.data.get('password')
    print(request.data.get('username'))
    # 调用django进行用户认证
    # 验证成功 user返回<class 'django.contrib.auth.models.User'>
    # 验证失败 user返回None
    user = auth.authenticate(username=username, password=password)
    if user == None:
        result = False
        errorInfo = u'用户名或密码错误'
        return Response({"result": result, "detail": detail, "errorInfo": errorInfo})

    # 用户名和密码验证成功
    # 获取用户的token 如果没有token ，表示时用户首次登录，则进行创建，并且返回token
    try:
        tokenObj = Token.objects.get(user_id=user.id)
    except Exception as e:
        token=generate_random_str()
        # token 不存在 说明是首次登录
        tokenObj = Token.objects.create(user=user, key=token)
    # 获取token字符串
    token = tokenObj.key
    return Response({"result": result, "detail": {'token': token}, "errorInfo": errorInfo})


def generate_random_str(randomlength=32):
  """
  生成一个指定长度的随机字符串
  """
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789@=!'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str
