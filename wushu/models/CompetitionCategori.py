from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.TaoluCategory import TaoluCategory


# from wushu.models.CategoryItem import CategoryItem


class CompetitionCategori(models.Model):
    categori = models.ForeignKey(TaoluCategory, on_delete=models.CASCADE, verbose_name='Categori')
    athlete = models.ManyToManyField(Athlete)

    def __str__(self):
        return '%s' % (self.categori.categoryName)

    # yearcategori = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, verbose_name='YearCategori')
    # class Meta:
    #     default_permissions = ()
