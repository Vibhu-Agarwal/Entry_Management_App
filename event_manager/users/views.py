from bcrypt import checkpw
from django.conf import settings
from users.forms import HostSignUpForm
from management.models import ManagementTokenAuth
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from users.permissions import LoggedOutRequiredMixin
from django.core.exceptions import PermissionDenied

HOST_REPR = settings.HOST_REPR


class HostSignUpView(LoggedOutRequiredMixin, FormView):
    template_name = 'host_sign_up.html'
    success_url = '/me'
    form_class = HostSignUpForm

    def verified_em_token(self, management_token, token_host_email):
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
