from django.core.mail import mail_admins, send_mail,EmailMessage,BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    # try :
        # i put these for a reference to emails        

        # message = EmailMessage('subject','message','amr@gmail.com',['Rest@amr.com'])
        # message.attach_file('playground/static/images/test.jpeg')
        # message.send()
        # # mail_admins('subject','message',html_message='test')
        # # send_mail('subject','message','info@amr.com',['Rest@amr.com'])

    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name':'Amr'}
    #         )
    #     message.send(['rest@amr.com'])
    # except BadHeaderError:
    #     pass
    return render(request, 'hello.html', {'name': 'Amr'})
