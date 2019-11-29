from users.views import HostSignUpView, CustomLogoutView
from django.urls import path

app_name = "users"

urlpatterns = [
    path('host-signup/', HostSignUpView.as_view(), name='host_signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout')
]
