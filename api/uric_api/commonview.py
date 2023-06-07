from rest_framework import viewsets, permissions,mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
class P2(PageNumberPagination):
    page_size = 'page'  #每一页显示的条数
    page_query_param = 'page' #获取参数中传入的页码
    page_size_query_param = 'size' #获取url参数中每页显示的数据条数

    max_page_size = 400


  
