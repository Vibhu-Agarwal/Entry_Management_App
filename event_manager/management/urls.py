from management.views import MeView, NewVisitAndVisitorView, CheckOutView
from django.urls import path

app_name = 'management'

urlpatterns = [
    path('visit/new/', NewVisitAndVisitorView.as_view(), name='new_visit'),
    path('visit/checkout/<int:visit_id>/', CheckOutView.as_view(), name='checkout_visit'),
    path('me/', MeView.as_view(), name='home_page'),
]