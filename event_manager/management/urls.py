from management.views import MeView, NewVisitAndVisitorView
from django.urls import path

app_name = 'management'

urlpatterns = [
    path('visit/new/', NewVisitAndVisitorView.as_view(), name='new_visit'),

    path('me/', MeView.as_view(), name='home_page'),
]