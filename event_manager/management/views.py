from users.models import User
from visit.models import Visit
from management.models import ManagementTokenAuth
from bcrypt import gensalt, hashpw
from secrets import token_urlsafe
from django.conf import settings
from django.utils import timezone
from management.serializers import ManagementTokenAuthSerializer
from visit.serializers import (VisitSerializer, VisitAndVisitorSerializer,
                               UpdateVisitorVisitSerializer)
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from users.permissions import IsHostOrLoggedOutMixin, IsManagementMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from management.forms import (VisitVisitorModelForm, VisitModelForm,
                              ManagementTokenAuthForm)
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from management.mailing import send_host_signup_email

HOST_REPR = settings.HOST_REPR


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super(HomeView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Home'
        return context_data


class NewVisitAndVisitorView(IsHostOrLoggedOutMixin, FormView):
    template_name = 'new_visit.html'
    success_url = reverse_lazy('management:home_page')
    host_sign_in_url = reverse_lazy('login')

    def get_form_kwargs(self):
        kwargs = super(NewVisitAndVisitorView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'request_user': self.request.user})
        return kwargs

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return VisitModelForm
        else:
            return VisitVisitorModelForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            # Employee (Host)
            visit_data = form.cleaned_data
            visit_data['visitor'] = self.request.user.id
            visit_data['host'] = visit_data['host'].id
            visit_serializer = VisitSerializer(data=visit_data)
        else:
            # New Visitor
            visit_and_visitor_cleaned_data = form.cleaned_data

            visit_details = visit_and_visitor_cleaned_data['visit']
            visit_details['host'] = visit_details['host'].id
            visit_details['visitor'] = visit_and_visitor_cleaned_data['visitor']
            visit_serializer = VisitAndVisitorSerializer(data=visit_details)

        if visit_serializer.is_valid():
            visit = visit_serializer.save()
            login(self.request, visit.visitor)
        else:
            # Do something
            pass

        return super(NewVisitAndVisitorView, self).form_valid(form)

    def form_invalid(self, form):

        visitor_form = form.forms['visitor']
        visitor_form_errors = visitor_form.errors
        visitor_email_errors = visitor_form_errors.get('email', None)

        if visitor_email_errors:
            old_user_error = 'User with this Email address already exists.'

            if old_user_error in visitor_email_errors:

                # Removing old_user_error from visitor form errors
                visitor_form._errors['email'] = visitor_form.error_class()
                for visitor_email_error in visitor_email_errors:
                    if old_user_error != visitor_email_error:
                        visitor_form.add_error('email', visitor_email_error)
                length_visitor_email_errors = len(visitor_form_errors.get('email', None))

                if length_visitor_email_errors == 0:
                    visitor_form._errors.pop('email')
                    visitor_email = form.data['visitor-email']
                    visitor = User.objects.get(email=visitor_email)
                    if visitor.user_type == 'visitor':
                        # Old Visitor
                        visit_data = form.cleaned_data['visit']
                        visit_data['visitor'] = visitor.id
                        visit_data['host'] = visit_data['host'].id
                        visit_serializer = VisitSerializer(data=visit_data)

                        if visit_serializer.is_valid():
                            visit = visit_serializer.save()
                            login(self.request, visit.visitor)
                        else:
                            # Do something
                            pass

                        return super(NewVisitAndVisitorView, self).form_valid(form)
                    elif visitor.user_type == HOST_REPR:
                        # Visitor is an office employee
                        new_visit_path = self.request.path
                        sign_up_url = f"{str(self.host_sign_in_url)}?next={new_visit_path}"
                        return HttpResponseRedirect(sign_up_url)
                    else:
                        # Visitor is someone from management
                        raise PermissionDenied()
        return super(NewVisitAndVisitorView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context_data = super(NewVisitAndVisitorView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Visitor | New Visit'
        return context_data


class CheckOutView(LoginRequiredMixin, TemplateView):
    template_name = 'check_out.html'
    success_url = reverse_lazy('management:home_page')

    def post(self, request, *args, **kwargs):
        logged_in_user = self.request.user
        visit = logged_in_user.get_current_visitor_visit
        if not visit:
            return HttpResponse("No Visit to Check-out", status=422)
        if logged_in_user in (visit.visitor, visit.host):
            serializer = UpdateVisitorVisitSerializer(visit, data={}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(out_time=timezone.now())
            return HttpResponseRedirect(self.success_url)
        else:
            raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context_data = super(CheckOutView, self).get_context_data(**kwargs)
        logged_in_user = self.request.user
        visit = logged_in_user.get_current_visitor_visit
        if visit is not None:
            context_data['visit_data'] = visit
        context_data['page_title'] = 'Visit Checkout'
        return context_data


class ManagementTokenAuthView(LoginRequiredMixin, IsManagementMixin, FormView):
    template_name = 'management/new_host.html'
    success_url = reverse_lazy('management:home_page')
    form_class = ManagementTokenAuthForm
    host_sign_up_url = reverse_lazy('users:host_signup')

    def form_valid(self, form):
        manager = self.request.user
        host_email = form.cleaned_data['host_email']
        users_with_provided_email = User.objects.filter(email=host_email)
        if users_with_provided_email.exists():
            user_with_provided_email = users_with_provided_email.first()
            if user_with_provided_email.user_type == 'visitor':
                # Work, if want to convert Visitor to Host
                pass
            return HttpResponse("User Already Created", status=406)
        while True:
            generated_token = token_urlsafe()
            hashed_token = hashpw(generated_token.encode('utf8'), gensalt())
            dup_token_auths = ManagementTokenAuth.objects.filter(token_given=hashed_token)
            if not dup_token_auths.exists():
                break
            elif dup_token_auths.filter(token_used=True).exists():
                break
        management_token_auth_data = {
            'manager': manager.id,
            'host_email': host_email,
            'token_given': hashed_token.decode()
        }
        management_token_auth_ser = ManagementTokenAuthSerializer(data=management_token_auth_data)
        if management_token_auth_ser.is_valid():
            if settings.ALLOW_EMAILS:
                signup_absolute_url = self.request.build_absolute_uri(str(self.host_sign_up_url))
                registration_form_link = f"{signup_absolute_url}?em_token_email={host_email}&em_token={generated_token}"
                send_host_signup_email(host_email, registration_form_link)
                management_token_auth_ser.save()
            else:
                return HttpResponse("Emails not Allowed", status=503)
        else:
            # Do Something
            pass
        return super(ManagementTokenAuthView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(ManagementTokenAuthView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Manager | Create New Host'
        return context_data
