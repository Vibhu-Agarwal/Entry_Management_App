from django.contrib.auth.forms import UserCreationForm
from users.models import User


class HostSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number',
                  'office_branch', 'password1', 'password2')
