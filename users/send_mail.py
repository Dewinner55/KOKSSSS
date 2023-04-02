from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(user, code):
    send_mail(
        'ЗДРАСТВУЙТЕ, АКТИВИРУЙТЕ ВАШ АККАУНТ!',
        f'ЧТОБЫ АКТИВИРОВАТЬ ВАШ АККАУНТ, НЕОБХОДИМО ВВЕСТИ КОД:\n'
        f'{code}\n'
        f'НЕ ПЕРЕДАВАЙТЕ ЭТОТ КОД НИКОМУ!',
        'evelbrus55@gmail.com',
        [user],
        fail_silently=False,
    )

def atcviatetrue(email):
    subject = "Добро пожаловать на HOSTEL"
    message = f"Мы рады вас привествовать на нашем сайте\n Все предоставленные квартиры вы сможете посмотреть на нашем сайте по ссылке: http://127.0.0.1:8000/apartments/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)



def send_password_reset_email(email, token):
    subject = "Сброс пароля"
    message = f"Для сброса пароля примените код подтверждения \n{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

