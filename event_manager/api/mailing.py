from mail_templated import send_mail
from users.models import User
from visit.models import Visit
from visit.serializers import CreateVisitorVisitSerializer
from django.conf import settings


def send_host_email(visit_serializer: CreateVisitorVisitSerializer, visitor: User):
    visit_data = visit_serializer.validated_data
    in_time = visit_data['in_time']
    purpose = visit_data.get('purpose')
    host_email = [visit_data['host'].email]
    visitor_name = str(visitor)
    visitor_email = visitor.email
    visitor_phone = visitor.phone_number
    email_subject = f'Visitor Details | {visitor_name}'

    visitor_data = {
        'Visitor': visitor_name,
        'Email': visitor_email,
        'Phone': visitor_phone,
        'Check-In Time': in_time,
        'Purpose': purpose
    }
    send_mail(template_name='host_email.html',
              context={
                  'email_subject': email_subject,
                  'visitor_data': visitor_data,
              },
              from_email=settings.EMAIL_HOST, recipient_list=host_email)


def send_visitor_checkout_email(visit_instance: Visit):
    pass
