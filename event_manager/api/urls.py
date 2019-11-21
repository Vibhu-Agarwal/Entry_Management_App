from api.views import (ListHostsAPIView, ListVisitorsAPIView,
                       CreateHostAPIView, CreateVisitorAPIView,
                       CreateVisitAPIView,
                       HostVisitsAPIView, VisitorVisitsAPIView)

from django.urls import path

app_name = 'api'

urlpatterns = [
    path('hosts/', ListHostsAPIView.as_view(), name='hosts_list'),
    path('hosts/new/', CreateHostAPIView.as_view(), name='create_host'),

    path('visitors/', ListVisitorsAPIView.as_view(), name='visitors_list'),
    path('visitors/new/', CreateVisitorAPIView.as_view(), name='create_visitor'),

    path('visit/new/', CreateVisitAPIView.as_view(), name='create_visit'),

    path('visits/host/', HostVisitsAPIView.as_view(), name='user_host_visits_list'),
    path('visits/visitor/', VisitorVisitsAPIView.as_view(), name='user_visitor_visits_list'),
]
