from django.conf import settings
from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
from django.utils.functional import lazy as lazy_choices
from django.utils.translation import ugettext_lazy as _
HOST_REPR = settings.HOST_REPR


def get_host_choices_list():
    choices_list = []
    hosts = User.objects.filter(user_type=HOST_REPR)
    for host in hosts:
        choices_list.append((host.id, str(host)))
    return choices_list


class Visit(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitor_visits')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_visits')
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('visit')
        verbose_name_plural = _('visits')

    def __init__(self, *args, **kwargs):
        super(Visit, self).__init__(*args, **kwargs)
        self._meta.get_field('host').choices = lazy_choices(get_host_choices_list, list)()

    def __str__(self):
        return f'{self.visitor} -> {self.host}'

    def clean(self):
        if self.visitor.email == self.host.email:
            raise ValidationError('Host cannot be the same as Visitor')
        if self.in_time >= self.out_time:
            raise ValidationError('Exit time must be greater than entry time')
        if self.host.user_type != HOST_REPR:
            raise ValidationError('Host must be an office employee')
        super().clean()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.clean()
        super(Visit, self).save()
