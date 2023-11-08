import os
from dotenv import load_dotenv

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from store.signals import order_created
from ..models import User

load_dotenv()

@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Create the email message
        subject = "Welcome"
        from_email = os.getenv('EMAIL_FROM')
        to = [instance.email]

        context = {'first_name': instance.first_name}

        # Load your HTML template
        html_content = render_to_string("emails/welcome_template.html", context)

        # Create a plain text version
        text_content = "Welcome to Storefront, we're glad to have you.\n" \
                      "If you need any help with ordering your products, " \
                      "please don't hesitate to contact us!\n" \
                      "CEO, Amr Elkfrawy"

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
