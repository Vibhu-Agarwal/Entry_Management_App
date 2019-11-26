from django import forms
from users.models import User
from visit.models import Visit
from django.conf import settings
from django.forms import ValidationError
from betterforms.multiform import MultiModelForm

HOST_REPR = settings.HOST_REPR


class VisitModelForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['in_time', 'purpose', 'host']


class VisitorModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']


class VisitVisitorModelForm(MultiModelForm):
    form_classes = {
        'visitor': VisitorModelForm,
        'visit': VisitModelForm,
    }
