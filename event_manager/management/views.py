from users.models import User
from django.conf import settings
from visit.serializers import VisitSerializer, VisitAndVisitorSerializer
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from users.permissions import IsHostOrLoggedOutMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from management.forms import VisitVisitorModelForm, VisitorModelForm, VisitModelForm
from django.views.generic.edit import FormView

HOST_REPR = settings.HOST_REPR


class MeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = str(self.request.user)
        return context


class NewVisitAndVisitorView(IsHostOrLoggedOutMixin, FormView):
    template_name = 'new_visit.html'
    success_url = '/me'
    employee_sign_in_page = '/sign-in/'

    def get_user(self):
        user = self.request.user
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
        return user

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return VisitModelForm
        else:
            return VisitVisitorModelForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            # Employee (Host)
            visit_data = form.cleaned_data
            visit_data['visitor'] = self.get_user().id
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
                        user = User.objects.get(email=visitor_email)
                        login(self.request, user)

                        # Calling API
                        return super(NewVisitAndVisitorView, self).form_valid(form)
                    elif visitor.user_type == HOST_REPR:
                        # Visitor is an office employee
                        return HttpResponseRedirect(self.employee_sign_in_page)
                    else:
                        # Visitor is someone from management
                        raise PermissionDenied()
        return super(NewVisitAndVisitorView, self).form_invalid(form)
