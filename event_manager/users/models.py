from .managers import CustomUserManager
from django.conf import settings
from django.utils import timezone
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
        address_string = f"{self.name},"
        address_string += f"\n{self.address1},"
        if self.address2:
            address_string += f"\n{self.address2},"
        address_string += f"\n{self.city}-{self.zip_code},"
        address_string += f"\n{self.country}."
        return address_string


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

    def host_slot_status(self, requested_in_time, requested_out_time=None):
        available, msg = True, "Available"
        requested_in_date = requested_in_time.date()
        if settings.SINGLE_VISITOR:
            host_visits = self.host_visits.all().filter(in_time__date=requested_in_date)

            checked_out_host_visits = host_visits.filter(out_time__gt=requested_in_time)
            only_checked_in_host_visits = host_visits.filter(out_time__isnull=True)

            if requested_out_time:
                checked_out_host_visits = checked_out_host_visits.filter(in_time__lt=requested_out_time)
                only_checked_in_host_visits = only_checked_in_host_visits.filter(in_time__lt=requested_out_time)

            if checked_out_host_visits.exists() or only_checked_in_host_visits.exists():
                available, msg = False, "Checked-In"
            else:
                available, msg = self.visitor_slot_status(requested_in_time, requested_out_time)
        return available, msg

    def visitor_slot_status(self, requested_in_time, requested_out_time=None):
        available, msg = True, "Available"
        requested_in_date = requested_in_time.date()
        if settings.SINGLE_VISITOR:
            visitor_visits = self.visitor_visits.all().filter(in_time__date=requested_in_date)

            checked_out_visitor_visits = visitor_visits.filter(out_time__gt=requested_in_time)
            only_checked_in_visitor_visits = visitor_visits.filter(out_time__isnull=True)

            if requested_out_time:
                checked_out_visitor_visits = checked_out_visitor_visits.filter(in_time__lt=requested_out_time)
                only_checked_in_visitor_visits = only_checked_in_visitor_visits.filter(in_time__lt=requested_out_time)

            if checked_out_visitor_visits.exists() or only_checked_in_visitor_visits.exists():
                available, msg = False, "Un-available"
        return available, msg

    @property
    def get_current_host_visit(self):
        now = timezone.now()
        host_visits = self.host_visits.all().filter(in_time__lte=now).order_by('-in_time')
        if host_visits.exists():
            last_host_visit = host_visits.first()
            if last_host_visit.out_time:
                if last_host_visit.out_time > now:
                    return last_host_visit
            else:
                return last_host_visit
        return None

    @property
    def get_current_visitor_visit(self):
        now = timezone.now()
        visitor_visits = self.visitor_visits.all().filter(in_time__lte=now).order_by('-in_time')
        if visitor_visits.exists():
            last_visitor_visit = visitor_visits.first()
            if last_visitor_visit.out_time:
                if last_visitor_visit.out_time > now:
                    return last_visitor_visit
            else:
                return last_visitor_visit
        return None

    @property
    def get_current_visit(self):
        if self.user_type == HOST_REPR:
            current_host_visit = self.get_current_host_visit
            if current_host_visit is not None:
                return current_host_visit
        return self.get_current_visitor_visit

    @property
    def is_visit_as_visitor_ongoing(self):
        visit = self.get_current_visitor_visit
        if visit is not None:
            return True
        return False

    @property
    def is_visit_ongoing(self):
        visit = self.get_current_visit
        if visit is not None:
            return True
        return False

    @property
    def different_visitor_visits(self):
        now = timezone.now()
        visitor_visits = self.visitor_visits.all()
        current_visitor_visit = self.get_current_visitor_visit
        if current_visitor_visit:
            visitor_visits = visitor_visits.exclude(id=current_visitor_visit.id)
        planned_visits = visitor_visits.filter(in_time__gt=now)
        past_visits = visitor_visits.difference(planned_visits)
        return past_visits, current_visitor_visit, planned_visits

    @property
    def different_host_visits(self):
        now = timezone.now()
        host_visits = self.host_visits.all()
        current_host_visit = self.get_current_host_visit
        if current_host_visit:
            host_visits = host_visits.exclude(id=current_host_visit.id)
        planned_visits = host_visits.filter(in_time__gt=now)
        past_visits = host_visits.difference(planned_visits)
        return past_visits, current_host_visit, planned_visits

    @property
    def is_host(self):
        return self.user_type == HOST_REPR
