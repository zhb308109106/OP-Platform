from django_filters.rest_framework import FilterSet
import django_filters
from .models import Device
class DeviceFilter(FilterSet):
    """
    ip过滤器，模糊查询
    """
    server_ip = django_filters.CharFilter(field_name='server_ip', lookup_expr='icontains')  # icontains，包含且忽略大小写

    class Meta:
        # 指定模型
        models = Device
        # 指定需要模糊查询的字段
        fields = ['server_ip']
