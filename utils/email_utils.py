from operator import itemgetter
from django.shortcuts import render
from threading import Thread
from typing import Callable
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail as SendMail
from django.template.loader import render_to_string
from .smtp import SendMail as Smtp_SendMail
import logging
import locale
from datetime import datetime
from urllib.parse import urlparse


logger = logging.getLogger(__name__)

class InvalidUserModel(Exception):
    """The member model you provided is invalid"""
    pass

class EmailTemplateNotFound(Exception):
    """No email template found"""
    pass

class NotAllFieldCompiled(Exception):
    """Compile all the fields in the settings"""
    pass


def my_functional_view(request, member):
    # send_email(member)
    return render('/email/verify/')

def _get_validated_field(field, default_type=None):
    if default_type is None:
        default_type = str
    try:
        d = getattr(settings, field)
        if d == "" or d is None or not isinstance(d, default_type):
            raise AttributeError
        return d
    except AttributeError:
        raise NotAllFieldCompiled(f"Field {field} missing or invalid")


def get_member_password_email_context(member):
    sender = _get_validated_field('EMAIL_FROM_ADDRESS')
    domain = _get_validated_field('EMAIL_PAGE_DOMAIN')
    subject = _get_validated_field('EMAIL_PASSWORD_GENERATE_MAIL_SUBJECT')
    domain += '/' if not domain.endswith('/') else ''
    site_domain = urlparse(domain).netloc
    receiver_name = member.full_name()
    context = {
        'member': member,
        'subject': subject,
        'sender': sender,
        'receiver_name': receiver_name,
        'site_url': domain,
        'site_domain': site_domain
    }
    return context

def send_email_member_password(member, thread=True):
    mail_plain = _get_validated_field('EMAIL_PASSWORD_GENERATE_MAIL_PLAIN')
    mail_html = "../templates/" + _get_validated_field('EMAIL_PASSWORD_GENERATE_MAIL_HTML')
    context = get_member_password_email_context(member)

    args = (member, context['sender'], context['subject'], mail_plain, mail_html, context)
    if thread:
        t = Thread(target=send_email_thread, args=args)
        t.start()
    else:
        send_email_thread(*args)

def send_email_thread(member, sender, subject, mail_plain, mail_html, context):   
    text = render_to_string(mail_plain, context)
    html = render_to_string(mail_html, context)
    password = _get_validated_field('EMAIL_HOST_PASSWORD')
    try:
        Smtp_SendMail(subject, text, html, sender, member.email, password)
    except Exception as ex:
        logger.warning(' ==== Failed to send email: id = %d: %s (%s)', 
            member.id,
            str(ex),
            type(ex)
        )
        return False
    logger.info(' ==== Sent an email successfully: member id = %d', member.id)
    return True
