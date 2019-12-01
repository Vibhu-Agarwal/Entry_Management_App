# Models
from users.models import User
from visit.models import Visit
from management.models import ManagementTokenAuth
# Serializers
from management.serializers import ManagementTokenAuthSerializer
from visit.serializers import (VisitSerializer, VisitAndVisitorSerializer,
                               UpdateVisitorVisitSerializer)
# Hashers
from bcrypt import gensalt, hashpw
from secrets import token_urlsafe
# django utilities
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
# Responses and Exceptions
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
# Permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from users.permissions import (IsHostOrLoggedOutMixin, IsHostMixin,
                               IsManagementMixin, IsNotManagementMixin)
# Views
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
# Forms
from visit.forms import VisitModelForm
from users.forms import OfficeBranchForm
from management.forms import (VisitVisitorModelForm, ManagementTokenAuthForm)
# Mailing
from management.mailing import send_host_signup_email


class HomeView(TemplateView):
    """
    View to render Home Page of the Application
    """

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super(HomeView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Home'
        return context_data


class ListHostVisitsView(LoginRequiredMixin, IsHostMixin, TemplateView):
    """
    View to List Visits of a person, in which he/she participated as a Host
    """
    template_name = 'host_visits.html'

    def get_visit_context_dict(self, past_visits, current_visit, planned_visits):
        """
        Function to create a dictionary for context data, that contains visits
        as requested in URL query parameters ('visit_type')
        :param past_visits: Queryset of past Visits of a person
        :param current_visit:  Queryset of Ongoing Visit of a person
        :param planned_visits:  Queryset of planned or future Visits of a person
        :return: Dictionary containing queryset of requested visit_type Visits
                    in 'all_visits' key
        """
        context_data = {}
        visit_type = self.request.GET.get('visit_type', None)
        if visit_type:
            if visit_type == 'past':
                context_data['visits_header'] = "Past Visits"
                context_data['all_visits'] = past_visits.order_by('-in_time')
            elif visit_type == 'ongoing':
                context_data['visits_header'] = "Ongoing Visit"
                if current_visit:
                    context_data['all_visits'] = Visit.objects.filter(id=current_visit.id)
                else:
                    context_data['all_visits'] = Visit.objects.none()
            elif visit_type == 'planned':
                context_data['visits_header'] = "Planned Visits"
                context_data['all_visits'] = planned_visits.order_by('in_time')
            else:
                context_data['visits_header'] = "Visits"
                context_data['all_visits'] = Visit.objects.none()
        else:
            context_data['visits_header'] = "All Visits"
            context_data['all_visits'] = past_visits.union(planned_visits).order_by('-in_time')
        return context_data

    def get_context_data(self, **kwargs):
        context_data = super(ListHostVisitsView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Host | Visits'
        logged_in_user = self.request.user
        past_visits, current_host_visit, planned_visits = logged_in_user.different_host_visits
        host_visits_data = self.get_visit_context_dict(past_visits, current_host_visit, planned_visits)
        context_data.update(host_visits_data)
        return context_data


class ListVisitorVisitsView(LoginRequiredMixin, IsNotManagementMixin, TemplateView):
    """
    View to List Visits of a person, in which he/she participated as a Visitor
    """
    template_name = 'visitor_visits.html'

    def get_visit_context_dict(self, past_visits, current_visit, planned_visits):
        """
        Function to create a dictionary for context data, that contains visits
        as requested in URL query parameters ('visit_type')
        :param past_visits: Queryset of past Visits of a person
        :param current_visit:  Queryset of Ongoing Visit of a person
        :param planned_visits:  Queryset of planned or future Visits of a person
        :return: Dictionary containing queryset of requested visit_type Visits
                    in 'all_visits' key
        """
        context_data = {}
        visit_type = self.request.GET.get('visit_type', None)
        if visit_type:
            if visit_type == 'past':
                context_data['visits_header'] = "Past Visits"
                context_data['all_visits'] = past_visits.order_by('-in_time')
            elif visit_type == 'ongoing':
                context_data['visits_header'] = "Ongoing Visit"
                if current_visit:
                    context_data['all_visits'] = Visit.objects.filter(id=current_visit.id)
                else:
                    context_data['all_visits'] = Visit.objects.none()
            elif visit_type == 'planned':
                context_data['visits_header'] = "Planned Visits"
                context_data['all_visits'] = planned_visits.order_by('in_time')
            else:
                context_data['visits_header'] = "Visits"
                context_data['all_visits'] = Visit.objects.none()
        else:
            context_data['visits_header'] = "All Visits"
            context_data['all_visits'] = past_visits.union(planned_visits).order_by('-in_time')
        return context_data

    def get_context_data(self, **kwargs):
        context_data = super(ListVisitorVisitsView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Visitor | Visits'
        logged_in_user = self.request.user
        past_visits, current_visitor_visit, planned_visits = logged_in_user.different_visitor_visits
        visitor_visit_data = self.get_visit_context_dict(past_visits, current_visitor_visit, planned_visits)
        context_data.update(visitor_visit_data)
        return context_data


class NewVisitAndVisitorView(IsHostOrLoggedOutMixin, FormView):
    """
    Main View of the application, handling forms for New Visit entry
    for New Visitors, Old Visitors and Employees trying to make a new Visit.

    This view also handles the request made by management to
    make a new Visit request and returns appropriate response in return.

    Only Accessible if the no one is logged-in or it's an office employee.
    """
    template_name = 'new_visit.html'
    success_url = reverse_lazy('management:home_page')
    host_sign_in_url = reverse_lazy('login')

    def get_form_kwargs(self):
        """
        Function to update provided keyword arguments so that
        corresponding New-Visit form is able to fetch current logged-in user data

        :return: Updated keyword arguments dict with 'request_user'
                    being instance of logged-in user
        """
        kwargs = super(NewVisitAndVisitorView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'request_user': self.request.user})
        return kwargs

    def get_form_class(self):
        """
        Function to fetch and render appropriate Form,
        according to the type of user logged-in

        :return: Returns concise form if the user is already authenticated,
                    that is, it's an employee logged in
                Returns elaborate form if no one is logged in,
                    asking to enter the details of the user as well
        """
        if self.request.user.is_authenticated:
            return VisitModelForm
        else:
            return VisitVisitorModelForm

    def form_valid(self, form):
        """
        Function called if a New Visitor or a logged-in Employee
        correctly filled out all the details on the New-Visit form

        :param form: instance of the form rendered on front-end,
                        with data filled by entries made by the user
        :return: A Redirection response to the success_url specified by the View
        """
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

        return super(NewVisitAndVisitorView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Function is called in four cases:
        1) An old visitor correctly fills out the form
        2) An office employee tries to fill out the form in logged-out state
        3) Someone from management tries to fill out the form in logged-out state
        4) Form is filled incorrectly

        :param form: form with incorrect details filtered out,
                        as specified by Multi-Model form
        :return: 1) A Redirection response to the success_url specified by the View
                 2) A Redirection response to the Host Sign-In page
                 3) Forbidden response
                 4) Rendering of the form on front-end, displaying incorrect filled entries
        """
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

                # If there was ONLY old_user_error in visitor_email errors
                if length_visitor_email_errors == 0:
                    visitor_form._errors.pop('email')

                    # If the form HAD errors ONLY in Email Field
                    if len(form.errors) == 0:
                        visitor_email = form.data['visitor-email']
                        visitor = User.objects.get(email=visitor_email)

                        # Old Visitor Filled Out the form correctly
                        if visitor.user_type == 'visitor':
                            visit_data = form.cleaned_data['visit']
                            visit_data['visitor'] = visitor.id
                            visit_data['host'] = visit_data['host'].id
                            visit_serializer = VisitSerializer(data=visit_data)

                            # Data specified by form satisfies model constraints
                            if visit_serializer.is_valid():
                                visit = visit_serializer.save()
                                login(self.request, visit.visitor)

                            # Peforming action after successful form processing
                            return super(NewVisitAndVisitorView, self).form_valid(form)

                        # An Office employee tried to fill out the form
                        elif visitor.is_host:
                            new_visit_path = self.request.path
                            sign_up_url = f"{str(self.host_sign_in_url)}?next={new_visit_path}"

                            # Returning a Redirection response to the Host Sign-In page
                            return HttpResponseRedirect(sign_up_url)

                        # Someone from management tried to fill out the form
                        else:
                            raise PermissionDenied()
        # Form is filled incorrectly
        return super(NewVisitAndVisitorView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context_data = super(NewVisitAndVisitorView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Visitor | New Visit'
        return context_data


class OngoingVisitAndCheckOutView(LoginRequiredMixin, TemplateView):
    """
    View peforms two tasks:
    1) to show ongoing visit of a logged-in User
    2) handling check-out request for ongoing visit by the user
    """
    template_name = 'ongoing_visit.html'
    success_url = reverse_lazy('management:home_page')

    def post(self, request, *args, **kwargs):
        """
        Function to handle check-out request for ongoing visit by the user
        :param request: An instance of the request data
                        made throught POST method
        :return: Appropriate response after checking-out
                    the ongoing visit
        """
        logged_in_user = self.request.user
        visit = logged_in_user.get_current_visit
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
        """
        Function to fetch and render details of ongoing visit,
        based on logged-in user being an employee or a visitor

        :return: context_data dictionary to pass data to the templates
        """
        context_data = super(OngoingVisitAndCheckOutView, self).get_context_data(**kwargs)
        logged_in_user = self.request.user
        visit = logged_in_user.get_current_visit
        if visit is not None:
            if logged_in_user.is_host:
                visitor = visit.visitor
                visit_data = {
                    'Visitor': str(visitor),
                    'Email': visitor.email,
                    'Phone': visitor.phone_number,
                    'Check-In Time': visit.in_time,
                }
            else:
                host = visit.host
                visit_data = {
                    'Host': str(host),
                    'Email': host.email,
                    'Phone': host.phone_number,
                    'Check-In Time': visit.in_time,
                    'Address': str(host.office_branch),
                }
            if visit.purpose:
                visit_data['Purpose'] = visit.purpose
            context_data['visit_data'] = visit_data
        context_data['page_title'] = 'Ongoing Visit'
        return context_data


class ManagementTokenAuthView(LoginRequiredMixin, IsManagementMixin, FormView):
    """
    View to handle new host creation request made by someone from management.

    This View creates a new unique URL for manager to send to the person
    intended to be created as Host. The token is hashed using bcrypt and stored
    in the database.

    The unique Sign-Up URL link is sent to the intended person's mail.
    """
    template_name = 'management/new_host.html'
    success_url = reverse_lazy('management:home_page')
    form_class = ManagementTokenAuthForm
    host_sign_up_url = reverse_lazy('users:host_signup')

    def form_valid(self, form):
        """
        Function called if the manager enters a valid email to send
        unique sign-up URL

        :param form: instance of form filled with correct email of the person
        :return: Appropriate response after processing the form.
        """
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


class NewOfficeBranchView(LoginRequiredMixin, IsManagementMixin, FormView):
    template_name = 'management/new_office_branch.html'
    success_url = reverse_lazy('management:home_page')
    form_class = OfficeBranchForm

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(NewOfficeBranchView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(NewOfficeBranchView, self).get_context_data(**kwargs)
        context_data['page_title'] = 'Manager | New Office Branch'
        return context_data
