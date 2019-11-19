from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.db import models

from django.utils.translation import ugettext_lazy as _

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. "
                                     "Up to 15 digits allowed.")

USER_TYPE = (
    ('employee', 'Employee'),
    ('management', 'Management'),
    ('visitor', 'Visitor'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='static', null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=17)
    user_type = models.CharField(max_length=15, choices=USER_TYPE, default='visitor')
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('staff'))
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
