from django.db import models

from users.models import CustomUser

from rest_framework.permissions import BasePermission, SAFE_METHODS

from multiselectfield import MultiSelectField


class ApartmentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # Разрешить только владельцу квартиры изменять её
        return obj.user == request.user if obj.user else False



class Apartment(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=False,
                             default=None)
    street = models.CharField(verbose_name='Улица', max_length=200, blank=False)
    city = models.CharField(verbose_name='Город', max_length=100, blank=False)
    state = models.CharField(verbose_name='Округ', help_text='Необязательно поле для заполнения', max_length=100,
                             blank=True)
    rooms = models.IntegerField(help_text='напишите кол-во комнат', verbose_name='Количество комнат', default=0)
    number_of_beds = models.IntegerField(help_text='количество спальных мест в квартире', verbose_name='Количество мест', default=0)
    floor = models.IntegerField(help_text='на каком этаже находится ваша квартира', verbose_name='Этаж', default=1)
    category = models.CharField(help_text='Люкс,элитка,эконом', verbose_name='Категория жилья', max_length=255, default='')
    price = models.DecimalField(help_text='Напишите вашу цену', verbose_name='Цена', max_digits=10, decimal_places=2, default=0)

    WIFI = 'wi-fi'
    SHOWER = 'shower'
    DOORPHONE = 'doorphone'
    PARKING = 'parking'
    TV = 'tv'
    APPLIANCES = 'appliances'
    AC = 'ac'
    BEDDING = 'bedding'

    # COMFORT_CHOICES = [
    #     (WIFI, 'Wi-Fi'),
    #     (SHOWER, 'Душевая кабина'),
    #     (DOORPHONE, 'Домофон'),
    #     (PARKING, 'Парковка'),
    #     (TV, 'Телевизор'),
    #     (APPLIANCES, 'Бытовая техника'),
    #     (AC, 'Кондиционер'),
    #     (BEDDING, 'Постельное белье'),
    # ]

    COMFORT_CHOICES = [('wi-fi', 'Wi-Fi'),
                       ('shower', 'Душевая кабина'),
                       ('doorphone', 'Домофон'),
                       ('parking', 'Парковка'),
                       ('tv', 'Телевизор'),
                       ('appliances', 'Бытовая техника'),
                       ('ac', 'Кондиционер'),
                       ('bedding', 'Постельное белье'),
                    ]

    comfort = MultiSelectField(choices=COMFORT_CHOICES, max_length=200, default='')
    description = models.TextField(help_text='Опишите максимально', verbose_name='Описание', default='')
    images = models.ImageField(verbose_name='Фотографии', default='default.jpg', blank=True, upload_to='apartment_images')
    zip_code = models.CharField(verbose_name='Почтовый индекс', help_text='Необязательно поле для заполнения',
                                max_length=20, blank=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return f"{self.street}"

