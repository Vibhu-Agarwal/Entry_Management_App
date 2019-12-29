from mail_templated import send_mail
from visit.models import Visit
from django.conf import settings


def send_host_signup_email(host_email, signup_form_link):
    """
    Function to send mail to a person, enabling them to sign-up for a Host role.

    :param host_email: Email of person intended to be created host
    :param signup_form_link: Full Unique Link for the intended user
    :return: None
    """
    send_mail(template_name='mailing/host_sign_up_mail.html',
              context={
                  'email_subject': 'Host | Registration Link',
                  'form_link': signup_form_link,
              },
              from_email=settings.EMAIL_HOST, recipient_list=[host_email])


def send_host_checkin_email(visit_instance: Visit):
    """
    Function to send email to Host of a Visit on Check-In,
    informing about the Visitor Details
    :param visit_instance: an instance of Visit, being checked-in
    :return: None
    """
    visitor = visit_instance.visitor
    host = visit_instance.host
    in_time = visit_instance.in_time
    purpose = visit_instance.purpose
    host_email = [host.email]
    visitor_name = str(visitor)
    visitor_email = visitor.email
    visitor_phone = visitor.phone_number
    email_subject = f'Visitor Details | {visitor_name}'

    visitor_data = {
        'Visitor': visitor_name,
        'Email': visitor_email,
        'Phone': visitor_phone,
        'Check-In Time': in_time,
    }
    if purpose:
        visitor_data['Purpose'] = purpose
    send_mail(template_name='mailing/host_checkin_email.html',
              context={
                  'email_subject': email_subject,
                  'visitor_data': visitor_data,
              },
              from_email=settings.EMAIL_HOST, recipient_list=host_email)


def send_visitor_checkout_email(visit_instance: Visit):
    """
    Function to send email to visitor of a Visit on Check-out,
    informing about details of Visitor and Visit
    :param visit_instance:  an instance of Visit, being checked-out
    :return: None
    """
    visitor = visit_instance.visitor
    host = visit_instance.host
    email_subject = f"Visit Details | {host}"
    visitor_email = [visitor.email]
    visit_data = {
        'Host': str(host),
        'Email': host.email,
        'Phone': host.phone_number,
        'Check-In Time': visit_instance.in_time,
        'Check-Out Time': visit_instance.out_time,
        'Address': str(host.office_branch),
    }
    if visit_instance.purpose:
        visit_data['Purpose'] = visit_instance.purpose
    send_mail(template_name='mailing/visitor_checkout_email.html',
              context={
                  'email_subject': email_subject,
                  'visit_data': visit_data
              },
              from_email=settings.EMAIL_HOST, recipient_list=visitor_email)
