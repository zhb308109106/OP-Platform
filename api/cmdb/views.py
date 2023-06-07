from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import DeviceSerializer,UserSerializer
from .models import Device
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
from uric_api.commonview import P2
from rest_framework.pagination import PageNumberPagination
from .filters import DeviceFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from openpyxl import load_workbook
@permission_classes((permissions.IsAuthenticated,))
class DeviceView(viewsets.ModelViewSet):
  queryset = Device.objects.all()
  serializer_class = DeviceSerializer 
  pagination_class = P2 
  filterset_class = DeviceFilter
       

class UserView(viewsets.ModelViewSet):
   permission_classes = [permissions.AllowAny]
   queryset = User.objects.all() 
   serializer_class = UserSerializer

@permission_classes((permissions.AllowAny,))
class UploadView(APIView):
 
    def get(self,reqeust):
        return  Response("ok")
 
    def post(self,reqeust):
        put_file = reqeust.FILES.get("put_file")  #上传文件的post请求时，获取文件内容-->putfile
 
        with open(put_file.name,"wb") as f:   #将文件内容写入到文件中保存
            for line in put_file:
                f.write(line)
        wb = load_workbook(put_file.name)
        sh = wb.worksheets[0] 
        deviceList = []
        for i,val in enumerate(list(sh.rows)): 
          if i!=0:
            device_obj = Device(system_name=val[0].value,server_name=val[1].value,server_ip=val[2].value,app_admin=val[3].value,asset_ownership=val[4].value,server_type=val[5].value,purchase_date=val[6].value,expired_date=val[7].value,generate_account=val[8].value,generate_pwd=val[9].value,admin_account=val[10].value,admin_pwd=val[11].value)
            deviceList.append(device_obj)
        print(deviceList)
        Device.objects.bulk_create(deviceList)
        return Response('OK') 

