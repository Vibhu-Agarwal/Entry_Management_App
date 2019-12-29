from django.db import models
from users.models import User


class ManagementTokenAuth(models.Model):
    """
    Model to store details of unique links sent by managers of the application
    to create New Hosts

    manager: Points to instance of User(manager), who sent the unique link to the person

    host_email: Email-Id of the person, intended to be created as a host

    token_given: Hash of the token assigned to Sign-Up unique link for a person

    token_used: Boolean value, True indicating that token has been used by the person
                                False indicating that token is yet to be used by the person
    """
    manager = models.ForeignKey(User, related_name='management_token_auths',
                                limit_choices_to={'user_type': 'management'},
                                on_delete=models.CASCADE)
    host_email = models.EmailField(unique=True)
    token_given = models.CharField(max_length=100)
    token_used = models.BooleanField(default=False)
