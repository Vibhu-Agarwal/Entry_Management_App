from django.core.management.base import BaseCommand
from users.models import User, OfficeBranch
from django.conf import settings

email_superuser = 'superuser@emweb.in'
email_manager = 'manageruser@emweb.in'

help_message = f"""
Sets up the DB, creating:
1) superuser with admin rights (Email: {email_superuser})
2) Manager: Rights to add new Hosts (Email: {email_manager})
"""


class Command(BaseCommand):
    help = help_message

    def handle(self, *args, **kwargs):
        if not User.objects.filter(email=email_superuser).exists():
            User.objects.create_superuser(first_name="Super User", email=email_superuser,
                                          password=settings.EMAIL_HOST_PASSWORD)
        if not User.objects.filter(email=email_manager).exists():
            User.objects.create_user(first_name="Mr. Manager", email=email_manager, user_type='management',
                                     password=settings.EMAIL_HOST_PASSWORD)
        office_branches = OfficeBranch.objects.all()
        if office_branches.count() == 0:
            OfficeBranch.objects.create()
