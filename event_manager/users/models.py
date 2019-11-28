from .managers import CustomUserManager
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.db import models

from django.utils.translation import ugettext_lazy as _

DEFAULT_OFFICE_ADDRESS = settings.DEFAULT_OFFICE_ADDRESS

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. "
                                     "Up to 15 digits allowed.")

HOST_REPR = settings.HOST_REPR
USER_TYPE = (
    (HOST_REPR, 'Employee'),
    ('management', 'Management'),
    ('visitor', 'Visitor'),
)


class OfficeBranch(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=1024,
        default=DEFAULT_OFFICE_ADDRESS['name']
    )
    address1 = models.CharField(
        _("Address line 1"),
        max_length=1024,
        default=DEFAULT_OFFICE_ADDRESS['add1']
    )
    address2 = models.CharField(
        _("Address line 2"),
        max_length=1024,
        default=DEFAULT_OFFICE_ADDRESS['add2'],
        blank=True, null=True,
    )
    zip_code = models.CharField(
        _("ZIP / Postal code"),
        max_length=12,
        default=DEFAULT_OFFICE_ADDRESS['zip']
    )
    city = models.CharField(
        _("City"),
        max_length=1024,
        default=DEFAULT_OFFICE_ADDRESS['city']
    )
    country = models.CharField(
        _("Country"),
        max_length=1024,
        default=DEFAULT_OFFICE_ADDRESS['country']
    )

    class Meta:
        verbose_name = "Office Branch"
        verbose_name_plural = "Office Branches"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='static', null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=17)
    user_type = models.CharField(max_length=15, choices=USER_TYPE, default='visitor')
    office_branch = models.ForeignKey(OfficeBranch, blank=True, null=True,
                                      on_delete=models.CASCADE, related_name='employees')
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        user_representation = self.first_name
        if self.last_name:
            user_representation += f" {self.last_name}"
        return user_representation

    def clean(self):
        if self.user_type == HOST_REPR:
            if not self.office_branch:
                raise ValidationError("Employees Must be associated with an Office Branch")
        elif self.user_type == 'visitor':
            if self.office_branch:
                raise ValidationError("Visitors cannot have an Office Branch associated with them")
        super().clean()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.clean()
        except ValidationError as e:
            raise APIException(str(e))
        super(User, self).save()

    def slot_status(self, requested_in_time):
        available, msg = True, "Available"
        if settings.SINGLE_VISITOR:
            host_visits = self.host_visits.all()
            visitor_visits = self.visitor_visits.all()
            all_visits = host_visits.union(visitor_visits)
            for visit in all_visits:
                if visit.in_time < requested_in_time:
                    if visit.out_time:
                        if visit.out_time > requested_in_time:
                            available, msg = False, "Unavailable"
                            break
                    else:
                        available, msg = False, "Checked-In"
                        break
        return available, msg
