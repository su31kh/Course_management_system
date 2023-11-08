from django.core.mail import send_mail
from django.conf import settings

def send_email_to_client(email, code):
    subject = "Email Verification Code"
    message = "The verification code for your account is " + str(code)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [ email ]
    send_mail(subject, message, from_email, recipient_list)
