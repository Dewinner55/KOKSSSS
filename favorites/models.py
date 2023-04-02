from django.db import models


from Apartment.models import Apartment
from users.models import CustomUser


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, verbose_name='Аппартаменты', on_delete=models.CASCADE)
    favorites = models.CharField(verbose_name='Избранное', max_length=200)
    is_favorite = models.BooleanField(verbose_name='В избранном', default=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f"{self.favorites}"
