from api.views import HostsAPIView, HostVisitsAPIView, VisitorVisitsAPIView

from django.urls import path

app_name = 'api'

urlpatterns = [
    path('hosts/', HostsAPIView.as_view(), name='hosts_list'),

    path('host_visits/', HostVisitsAPIView.as_view(), name='host_visits_list'),
    path('visitor_visits/', VisitorVisitsAPIView.as_view(), name='visitor_visits_list'),
]