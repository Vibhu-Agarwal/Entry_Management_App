from django.conf import settings
from users.models import User

from rest_framework.serializers import BaseSerializer
from visit.serializers import (GETVisitSerializer, CreateVisitorVisitSerializer,
                               GETHostVisitSerializer, GETVisitorVisitSerializer,)
from users.serializers import (UserSerializer, HostCreateSerializer,
                               VisitorCreateSerializer)

from rest_framework.generics import ListAPIView, CreateAPIView

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from api.permissions import (IsVisitHost, IsVisitVisitor,
                             IsHostMixin, IsManagementMixin)

from api.mailing import send_host_email

HOST_REPR = settings.HOST_REPR


class ListHostsAPIView(LoginRequiredMixin, IsManagementMixin, ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(user_type=HOST_REPR)


class ListVisitorsAPIView(LoginRequiredMixin, IsManagementMixin, ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(user_type='visitor')


class CreateHostAPIView(LoginRequiredMixin, IsManagementMixin, CreateAPIView):
    serializer_class = HostCreateSerializer

    def perform_create(self, serializer: BaseSerializer):
        serializer.save(user_type=HOST_REPR)


class CreateVisitorAPIView(CreateAPIView):
    serializer_class = VisitorCreateSerializer

    def perform_create(self, serializer: BaseSerializer):
        serializer.save(user_type='visitor')


class CreateVisitAPIView(CreateAPIView):
    serializer_class = CreateVisitorVisitSerializer

    def perform_create(self, serializer: CreateVisitorVisitSerializer):
        visitor = self.request.user
        serializer.save(visitor=visitor)
        send_host_email(serializer, visitor)


class HostVisitsAPIView(LoginRequiredMixin, IsHostMixin, ListAPIView):
    serializer_class = GETHostVisitSerializer

    def get_queryset(self):
        host = self.request.user
        return host.host_visits.all()


class VisitorVisitsAPIView(LoginRequiredMixin, ListAPIView):
    serializer_class = GETVisitorVisitSerializer

    def get_queryset(self):
        visitor = self.request.user
        return visitor.visitor_visits.all()
