from users.views import HostSignUpView
from django.urls import path

app_name = "users"

urlpatterns = [
    path('host-signup/', HostSignUpView.as_view(), name='host_signup')
]
