from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from Apartment.models import Apartment
from users.models import CustomUser
import random
import string
from django.core.mail import send_mail


class Booking(models.Model):


    confirmation_code = models.CharField(max_length=6, blank=True)


    apartment = models.ForeignKey(Apartment, verbose_name='Аппартаменты', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    check_in = models.DateField(verbose_name='Въезд', blank=True)
    check_out = models.DateField(verbose_name='Выезд', blank=True)
    is_confirmed = models.BooleanField(verbose_name='Подтвержденно', default=False)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"{self.user}"

    def clean(self):
        # Проверка, чтобы дата заезда не была позднее даты выезда
        if self.check_in and self.check_out and self.check_in > self.check_out:
            raise ValidationError("Дата заезда не может быть позднее даты выезда.")

        # Проверка, чтобы даты не были в прошлом
        today = timezone.now().date()
        if self.check_in and self.check_in < today:
            raise ValidationError("Дата заезда не может быть в прошлом.")
        if self.check_out and self.check_out < today:
            raise ValidationError("Дата выезда не может быть в прошлом.")

    def is_apartment_available(self):
        # Проверка доступности квартиры для указанных дат
        overlapping_bookings = Booking.objects.filter(
            apartment=self.apartment,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
            is_confirmed=True
        )
        return not overlapping_bookings.exists()

    def save(self, *args, **kwargs):
        self.clean()
        if self.is_apartment_available():
            super().save(*args, **kwargs)
        else:
            raise ValidationError("Квартира уже забронирована на выбранные даты.")

    def generate_confirmation_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_confirmation_email(self):
        self.confirmation_code = self.generate_confirmation_code()
        self.save()

        subject = "Код подтверждения бронирования"
        message = f"Ваш код подтверждения для бронирования квартиры: {self.confirmation_code}"
        from_email = "evelbrus55@gmail.com"
        recipient_list = [self.user.email]

        send_mail(subject, message, from_email, recipient_list)

    def activate_booking(self, entered_code):

        subject = "Бронирование подтвержденно"
        message = f"Адресс: {self.apartment}, Въезд: {self.check_in}, выезд: {self.check_out}"
        from_email = "evelbrus55@gmail.com"
        recipient_list = [self.user.email]

        send_mail(subject, message, from_email, recipient_list)

        if self.confirmation_code == entered_code:
            self.is_confirmed = True
            self.save()
            return True
        else:
            return False

