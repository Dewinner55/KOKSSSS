from django.db import models


from Apartment.models import Apartment
from users.models import CustomUser


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    favorites = models.CharField(max_length=200)
    is_favorite = models.BooleanField(verbose_name='избранное', default=True)

    def __str__(self):
        return f"{self.favorites}"

