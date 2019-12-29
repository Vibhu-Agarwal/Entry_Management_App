from twilio.rest import Client
from django.conf import settings
from visit.models import Visit


account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_sender = settings.TWILIO_NUMBER

msg_template = """
Visit Details
Visitor: {visitor_name}
Email: {visitor_email}
Phone Number: {visitor_phone}
Check-in Time: {in_time}
"""


def send_host_checkin_sms(visit_instance: Visit):
    """
    Function to send an SMS to host on a Visit Check-in,
    informing about details of the Visitor
    :param visit_instance:  an instance of Visit, being checked-in
    :return: None
    """
    client = Client(account_sid, auth_token)

    visitor = visit_instance.visitor
    in_time = visit_instance.in_time
    visitor_name = str(visitor)
    visitor_email = visitor.email
    visitor_phone = visitor.phone_number
    msg = msg_template.format(in_time=in_time, visitor_name=visitor_name,
                              visitor_email=visitor_email, visitor_phone=visitor_phone)
    try:
        message = client.messages.create(
                             body=msg,
                             from_=twilio_sender,
                             to=visit_instance.host.phone_number
                         )
    except:
        print("SMS not sent!")
