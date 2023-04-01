
from django.db import models
from Apartment.models import Apartment
from users.models import CustomUser
# Create your models here.


class ApartmentsRating(models.Model):
    apartment = models.ForeignKey(Apartment, verbose_name='Квартира', on_delete=models.CASCADE, null=True, blank=False, default=None)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=False, default=None)
    rating = models.FloatField(verbose_name='оценка', help_text="Введите рейтинг от 1.0 до 5.0, например, 3.5")


    class Meta:
        verbose_name = 'Оценка квартиры'
        verbose_name_plural = 'Оценки квартир'

    def __str__(self):
        return f"{self.id} {self.apartment} {self.rating}"

    def save(self, *args, **kwargs):
        # Рассчитываем рейтинг на основе пятибальной системы
        if self.rating < 1.0:
            self.rating = 1.0
        elif self.rating > 5.0:
            self.rating = 5.0
        else:
            self.rating = round(self.rating * 2) / 2.0
        self.rating = round(self.rating, 2)
        super(ApartmentsRating, self).save(*args, **kwargs)
