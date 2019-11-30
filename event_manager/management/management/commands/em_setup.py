from django.core.management.base import BaseCommand
from users.models import User, OfficeBranch
from django.conf import settings


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        email_superuser = 'superuser@emweb.in'
        email_manager = 'manageruser@emweb.in'
        if not User.objects.filter(email=email_superuser).exists():
            User.objects.create_superuser(first_name="Super User", email=email_superuser,
                                          password=settings.EMAIL_HOST_PASSWORD)
        if not User.objects.filter(email=email_manager).exists():
            User.objects.create_user(first_name="Mr. Manager", email=email_manager, user_type='management',
                                     password=settings.EMAIL_HOST_PASSWORD)
        office_branches = OfficeBranch.objects.all()
        if office_branches.count() == 0:
            OfficeBranch.objects.create()
