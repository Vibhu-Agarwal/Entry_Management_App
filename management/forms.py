# Forms
from django import forms
from visit.forms import VisitModelForm
from users.forms import VisitorModelForm
from betterforms.multiform import MultiModelForm
# Models
from management.models import ManagementTokenAuth


class ManagementTokenAuthForm(forms.ModelForm):
    """
    Form for Management to Enter New User's email for creation
    """
    class Meta:
        model = ManagementTokenAuth
        fields = ['host_email']


class VisitVisitorModelForm(MultiModelForm):
    """
    Form for New and Old Visitors to make a new Visit
    """
    form_classes = {
        'visitor': VisitorModelForm,
        'visit': VisitModelForm,
    }
