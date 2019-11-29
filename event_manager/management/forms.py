from django import forms
from management.models import ManagementTokenAuth
from visit.forms import VisitModelForm
from users.forms import VisitorModelForm
from betterforms.multiform import MultiModelForm


class ManagementTokenAuthForm(forms.ModelForm):
    class Meta:
        model = ManagementTokenAuth
        fields = ['host_email']


class VisitVisitorModelForm(MultiModelForm):
    form_classes = {
        'visitor': VisitorModelForm,
        'visit': VisitModelForm,
    }
