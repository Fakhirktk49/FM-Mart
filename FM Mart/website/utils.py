from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
import threading

class EmailSenderThread(threading.Thread):
    def __init__(self,send_email):
        super().__init__()
        self.send_email=send_email

    def run(self):
        try:
            self.send_email.send(fail_silently=False)
        except Exception as e:
            print(e)

def email_sender(activation_url,email):
    try:
        subject=f'Activate your account on {settings.SITE_NAME}'
        to_email=[email]
        # from_email=['fakhirmasood49@gmail.com']
        html_content=render_to_string('website/activation_email.html',{'activation_url':activation_url})
        text_content=strip_tags(html_content)

        send_email=EmailMultiAlternatives(subject,text_content,to=to_email)
        send_email.attach_alternative(html_content,'text/html')
        EmailSenderThread(send_email).start()
    except Exception as e:
        print(f'Some exception occured in consructing email {e}')

def pass_reset_email_sender(activation_url,email):
    try:
        subject=f'Reset your password on {settings.SITE_NAME}'
        to_email=[email]
        html_content=render_to_string('website/password_reset_email.html',{'activation_url':activation_url})
        text_content=strip_tags(html_content)
        
        send_email=EmailMultiAlternatives(subject,text_content,to=to_email)
        send_email.attach_alternative(html_content,'text/html')
        EmailSenderThread(send_email).start()
    except Exception as e:
         print(f'Some exception occured in consructing email {e}')

