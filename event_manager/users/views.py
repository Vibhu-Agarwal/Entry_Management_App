# Hashsers
from bcrypt import checkpw
# django utilities
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Forms
from users.forms import HostSignUpForm
# Views
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
# Models
from management.models import ManagementTokenAuth
# permissions
from users.permissions import LoggedOutRequiredMixin
# Responses and Exceptions
from django.core.exceptions import PermissionDenied
# Serializers
from visit.serializers import UpdateVisitorVisitSerializer

HOST_REPR = settings.HOST_REPR


class HostSignUpView(LoggedOutRequiredMixin, FormView):
    """
    View to handle the request made by a person, got on by accessing
    unique Sign-Up URL sent by management.

    Renders the form on GET request to enter the details and
    Creates the host entry in the database on POST request.

    It checks the authenticity of the token used in the URL by
    extracting user email id on which the email was sent and comparing
    the token provided hash value with the one in the database.
    """
    template_name = 'host_sign_up.html'
    success_url = reverse_lazy('management:home_page')
    form_class = HostSignUpForm

    def verified_em_token(self, management_token, token_host_email):
        """
        Function to check authenticity of the token used in the URL
        :param management_token: token being used in the URL
        :param token_host_email: provided mail on which the mail must have
                                    been sent to
        :return: True if the token is valid, otherwise False
        """
        if management_token and token_host_email:
            management_token_auths_with_email = ManagementTokenAuth.objects.filter(host_email=token_host_email)
            if management_token_auths_with_email.exists():
                management_token_auth_with_email = management_token_auths_with_email.first()
                if not management_token_auth_with_email.token_used:
                    original_hashed_token = management_token_auth_with_email.token_given.encode('utf8')
                    management_token = management_token.encode('utf8')
                    if checkpw(management_token, original_hashed_token):
                        return True
        return False

    def get_context_data(self, **kwargs):
        management_token = self.request.GET.get('em_token', None)
        token_host_email = self.request.GET.get('em_token_email', None)
        if self.verified_em_token(management_token, token_host_email):
            context_data = super().get_context_data(**kwargs)
            context_data['em_token_value'] = management_token
            context_data['em_token_email_value'] = token_host_email
            context_data['page_title'] = 'Host | Sign-Up'
            return context_data
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        management_token = self.request.POST.get('em_token', None)
        token_host_email = self.request.POST.get('em_token_email', None)
        if self.verified_em_token(management_token, token_host_email):
            return super(HostSignUpView, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        if form.cleaned_data['user_type'] == HOST_REPR:
            form.save()
        else:
            user = form.save(commit=False)
            user.user_type = HOST_REPR
            user.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')

        management_token_auth = ManagementTokenAuth.objects.get(host_email=email)
        management_token_auth.token_used = True
        management_token_auth.save()
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        return super(HostSignUpView, self).form_valid(form)


class CustomLogoutView(LogoutView):
    """
    View to handle Log-out requests by users.

    If the logged-in user is not an Office-Employee, logging out of the app
    would also terminate the ongoing Visit session, if any.
    """

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logged_in_user = request.user
        visitor_visit = logged_in_user.get_current_visitor_visit
        if visitor_visit is not None:
            serializer = UpdateVisitorVisitSerializer(visitor_visit, data={}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(out_time=timezone.now())

        return super(CustomLogoutView, self).dispatch(request, *args, **kwargs)
