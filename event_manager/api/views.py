from django.conf import settings
from users.models import User, OfficeBranch

from django.utils import timezone

from rest_framework.serializers import BaseSerializer
from visit.serializers import (GETVisitSerializer, CreateVisitorVisitSerializer,
                               GETHostVisitSerializer, GETVisitorVisitSerializer,
                               UpdateVisitorVisitSerializer)
from users.serializers import (UserSerializer, HostCreateSerializer,
                               VisitorCreateSerializer, OfficeBranchSerializer)

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from django.contrib.auth.mixins import LoginRequiredMixin
from api.permissions import (IsVisitHost, IsVisitVisitor,
                             IsHostMixin, IsManagementMixin)

from api.mailing import send_host_email, send_visitor_checkout_email

HOST_REPR = settings.HOST_REPR


class CreateOfficeBranchAPIView(LoginRequiredMixin, IsManagementMixin, CreateAPIView):
    serializer_class = OfficeBranchSerializer


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


class CheckoutVisitAPIView(LoginRequiredMixin, UpdateAPIView):
    serializer_class = UpdateVisitorVisitSerializer
    permission_classes = (IsVisitVisitor,)

    def get_queryset(self):
        visitor = self.request.user
        return visitor.visitor_visits.all()

    def update(self, request, *args, **kwargs):
        visit_instance = self.get_object()
        update_response = super(CheckoutVisitAPIView, self).update(request, *args, **kwargs)
        response_serializer = GETVisitorVisitSerializer(visit_instance, update_response.data, partial=True)
        response_serializer.is_valid()
        return Response(response_serializer.data)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        visit_instance = self.get_object()
        serializer.save(out_time=timezone.now())
        send_visitor_checkout_email(visit_instance)


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
