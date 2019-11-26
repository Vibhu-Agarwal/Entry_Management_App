from api.views import (ListHostsAPIView, ListVisitorsAPIView,
                       CreateHostAPIView, CreateVisitorAPIView,
                       CreateHostVisitAPIView, CheckoutVisitAPIView,
                       HostVisitsAPIView, VisitorVisitsAPIView,
                       CreateVisitAndVisitorAPIView,
                       CreateOfficeBranchAPIView,
                       UserDetailAjaxAPIView)

from django.urls import path

app_name = 'api'

urlpatterns = [
    path('hosts/', ListHostsAPIView.as_view(), name='hosts_list'),
    path('hosts/new/', CreateHostAPIView.as_view(), name='create_host'),

    path('visitors/', ListVisitorsAPIView.as_view(), name='visitors_list'),
    path('visitors/new/', CreateVisitorAPIView.as_view(), name='create_visitor'),

    path('visit/new/host/', CreateHostVisitAPIView.as_view(), name='create_host_visit'),
    path('visit/new/', CreateVisitAndVisitorAPIView.as_view(), name='create_visit'),
    path('visit/checkout/<int:pk>/', CheckoutVisitAPIView.as_view(), name='checkout_visit'),

    path('visits/host/', HostVisitsAPIView.as_view(), name='user_host_visits_list'),
    path('visits/visitor/', VisitorVisitsAPIView.as_view(), name='user_visitor_visits_list'),

    path('office/branch/new/', CreateOfficeBranchAPIView.as_view(), name='new_office_branch'),

    path('user/detail/', UserDetailAjaxAPIView.as_view(), name='ajax_user_detail')
]
