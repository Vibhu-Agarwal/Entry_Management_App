from visit.serializers import (VisitSerializer, GETVisitSerializer,
                               GETHostVisitSerializer, GETVisitorVisitSerializer)
from users.serializers import UserSerializer
from visit.models import Visit
from users.models import User
from rest_framework.generics import ListAPIView
from api.permissions import (IsVisitHost, IsVisitVisitor,
                             IsHostMixin, IsManagementMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.mixins import LoginRequiredMixin


class HostsAPIView(LoginRequiredMixin, IsManagementMixin, ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(user_type='employee')


class HostVisitsAPIView(LoginRequiredMixin, IsHostMixin, ListAPIView):
    serializer_class = GETHostVisitSerializer

    def get_queryset(self):
        host = self.request.user
        return Visit.objects.filter(host=host)


class VisitorVisitsAPIView(LoginRequiredMixin, ListAPIView):
    serializer_class = GETVisitorVisitSerializer

    def get_queryset(self):
        visitor = self.request.user
        return Visit.objects.filter(visitor=visitor)
