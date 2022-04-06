from django.db import models

from wushu.models.Country import Country
from wushu.models.City import City


class Person(models.Model):
    MALE = 'MAN'
    FEMALE = 'WOMAN'

    AB1 = 'AB Rh+'
    AB2 = 'AB Rh-'
    A1 = 'A Rh+'
    A2 = 'A Rh-'
    B1 = 'B Rh+'
    B2 = 'B Rh-'
    O1 = '0 Rh+'
    O2 = '0 Rh-'

    GENDER_CHOICES = (
        (MALE, 'MAN'),
        (FEMALE, 'WOMAN'),
    )

    BLOODTYPE = (
        (AB1, 'AB Rh+'),
        (AB2, 'AB Rh-'),
        (A1, 'A Rh+'),
        (A2, 'A Rh-'),
        (B1, 'B Rh+'),
        (B2, 'B Rh-'),
        (O1, '0 Rh+'),
        (O2, '0 Rh-'),

    )

    pasaport = models.CharField(max_length=120, null=True, blank=True)
    pasaportImage = models.ImageField(upload_to='pasaport/', null=True, blank=True, default='pasaport/user.png',
                                      verbose_name='pasaport Picture')
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profile Picture')

    birthDate = models.DateField(null=True, blank=True, verbose_name='Birth Date')
    gender = models.CharField(max_length=128, verbose_name='Gender', choices=GENDER_CHOICES, default=MALE)

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke')
