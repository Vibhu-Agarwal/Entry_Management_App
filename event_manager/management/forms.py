from django import forms
from users.models import User
from visit.models import Visit
from management.models import ManagementTokenAuth
from django.conf import settings
from betterforms.multiform import MultiModelForm

HOST_REPR = settings.HOST_REPR


class ManagementTokenAuthForm(forms.ModelForm):
    class Meta:
        model = ManagementTokenAuth
        fields = ['host_email']


class VisitModelForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['in_time', 'purpose', 'host']

    def __init__(self, *args, **kwargs):
        if 'request_user' in kwargs:
            self.request_user = kwargs.pop('request_user')
        else:
            self.request_user = None

        super(VisitModelForm, self).__init__(*args, **kwargs)

        if self.request_user and self.request_user.is_authenticated and self.request_user.user_type == HOST_REPR:
            self.fields['host'].queryset = self.fields['host'].queryset.exclude(id=self.request_user.id)

    def clean(self):
        cleaned_data = super().clean()
        requested_in_time = cleaned_data['in_time']
        requested_host_user = cleaned_data['host']
        available, msg = requested_host_user.slot_status(requested_in_time)
        if not available:
            error_string = f"Host is {msg}"
            self.add_error('in_time', error_string)


class VisitorModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']


class VisitVisitorModelForm(MultiModelForm):
    form_classes = {
        'visitor': VisitorModelForm,
        'visit': VisitModelForm,
    }
