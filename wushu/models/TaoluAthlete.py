from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.Competition import Competition
from wushu.models.TaoluYearsCategory import TaoluYearsCategory
from wushu.models.TaoluCategory import TaoluCategory
from wushu.models.YearsTaoluCategory import YearsTaoluCategory


class TaoluAthlete(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    category = models.ForeignKey(TaoluCategory, on_delete=models.CASCADE)
    years = models.ForeignKey(YearsTaoluCategory, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.athlete.user.first_name, self.athlete.user.last_name)

    class Meta:
        default_permissions = ()
