from django import forms
from visit.models import Visit
from users.models import User
from betterforms.multiform import MultiModelForm


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
