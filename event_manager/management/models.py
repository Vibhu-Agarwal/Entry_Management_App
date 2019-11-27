from django.db import models
from users.models import User


class ManagementTokenAuth(models.Model):
    manager = models.ForeignKey(User, related_name='management_token_auths',
                                limit_choices_to={'user_type': 'management'},
                                on_delete=models.CASCADE)
    host_email = models.EmailField(unique=True)
    token_given = models.CharField(max_length=100)
    token_used = models.BooleanField(default=False)
