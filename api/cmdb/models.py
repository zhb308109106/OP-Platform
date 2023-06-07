from django.db import models
from django.utils import timezone
# Create your models here.


class Device(models.Model):
    system_name = models.CharField(max_length=1024)
    server_name = models.CharField(max_length=1024)
    server_ip = models.CharField(max_length=128,unique=True)
    app_admin = models.CharField(max_length=256,null=True)
    asset_ownership = models.CharField(max_length=256,null=True)
    server_type = models.CharField(max_length=128)
    purchase_date = models.DateTimeField('采购时间', null=True,default=timezone.now())
    expired_date = models.DateTimeField('过期时间', null=True,blank=True)
    generate_account = models.CharField(max_length=128,null=True,blank=True)
    generate_pwd = models.CharField(max_length=128,null=True,blank=True)
    admin_account = models.CharField(max_length=128,null=True,blank=True)
    admin_pwd = models.CharField(max_length=128,null=True,blank=True)
    

    class Meta:
        verbose_name = '服务器设备'
        verbose_name_plural = '服务器设备'
    
