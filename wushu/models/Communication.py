from django.db import models

from wushu.models.City import City
from wushu.models.Country import Country


class Communication(models.Model):

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='COUNTRY')

    class Meta:
        default_permissions = ()
