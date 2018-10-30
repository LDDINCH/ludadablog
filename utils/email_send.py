# _*_ encoding:utf-8 _*_
__author__ = "ludada"
__date__ = "2018/8/28 17:09"
from comment.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from ludadablog.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    Chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqWwSsZzXxVvYyTtRr1234567890'
    length = len(Chars)-1
    random = Random()
    for i in range(randomlength):
        str+= Chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type = 'register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '来自卢伟权的一封邮件'
        email_body = '请点击下面的链接激活验证码：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    else:
        email_title = '来自卢伟权的一封修改密码的邮件'
        email_body = '请点击下面的链接修改密码：http://127.0.0.1:8001/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
