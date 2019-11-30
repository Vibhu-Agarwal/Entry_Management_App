from django import forms
from django.conf import settings
from django.forms import HiddenInput
from django.contrib.auth.forms import UserCreationForm
from users.models import User

HOST_REPR = settings.HOST_REPR


class HostSignUpForm(UserCreationForm):
    """
    Form to handle the Sign-Up requests by the User,
    who is offered to be a Host by the manager
    """

    def __init__(self, *args, **kwargs):
        super(HostSignUpForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].initial = HOST_REPR

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number',
                  # 'office_branch', 'password1', 'password2')
                  'office_branch', 'user_type', 'password1', 'password2')
        widgets = {'user_type': HiddenInput()}


class VisitorModelForm(forms.ModelForm):
    """
    Form specifying the fields to be taken for input while creating a new Visitor
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']


