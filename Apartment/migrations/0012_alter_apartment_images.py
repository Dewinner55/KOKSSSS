# Generated by Django 4.1.7 on 2023-03-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Apartment", "0011_apartment_category_apartment_comfort_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartment",
            name="images",
            field=models.ImageField(
                blank=True,
                default="default.jpg",
                upload_to="",
                verbose_name="Фотографии",
            ),
        ),
    ]
