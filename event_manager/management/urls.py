from management.views import (HomeView, NewVisitAndVisitorView, ListVisitorVisitsView, ListHostVisitsView,
                              OngoingVisitAndCheckOutView, ManagementTokenAuthView)
from django.urls import path

app_name = 'management'

urlpatterns = [
    path('visit/new/', NewVisitAndVisitorView.as_view(), name='new_visit'),
    path('visits/visitor/', ListVisitorVisitsView.as_view(), name='visitor_visits_list'),
    path('visits/host/', ListHostVisitsView.as_view(), name='host_visits_list'),
    path('visits/ongoing/', OngoingVisitAndCheckOutView.as_view(), name='checkout_visit'),
    path('management/new-host/', ManagementTokenAuthView.as_view(), name='management_new_host'),
    path('', HomeView.as_view(), name='home_page'),
]