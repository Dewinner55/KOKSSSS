from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from booking.models import Booking

@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_booking_confirmation_email_task(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return

    # Создаем и отправляем подтверждающее письмо
    subject = 'Подтверждение бронирования квартиры'
    message = f'Уважаемый(-ая) {booking.user.first_name},\n\n' \
              f'Ваше бронирование квартиры "{booking.apartment.street}, {booking.apartment.city}" ' \
              f'с {booking.check_in} по {booking.check_out} на {booking.number_of_guests} гостей подтверждено.\n\n' \
              f'С уважением,\n\n' \
              f'Администрация сайта'

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.email]

    send_mail(subject, message, from_email, recipient_list)

    # Сохраняем запись в базе данных об отправленном письме
    Booking.objects.create(
        booking=booking,
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )