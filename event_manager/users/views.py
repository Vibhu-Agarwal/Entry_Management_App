from users.forms import HostSignUpForm
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from users.permissions import LoggedOutRequiredMixin


class HostSignUpView(LoggedOutRequiredMixin, FormView):
    template_name = 'host_sign_up.html'
    success_url = '/me'
    form_class = HostSignUpForm

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        return super(HostSignUpView, self).form_valid(form)
