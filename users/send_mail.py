from django.core.mail import send_mail


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