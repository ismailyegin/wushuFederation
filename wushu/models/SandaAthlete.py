from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.Competition import Competition


class SandaAthlete(models.Model):
    SANDA_YAS_TYPE = (
        (0, 'Sanda'),
        (1, 'Ligth Sanda'),
        (2, 'Tuishou'),

    )

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    competitiontype = models.CharField(max_length=128, verbose_name='Yaş Kategorisi', choices=SANDA_YAS_TYPE)
    athlete_yas_category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.athlete.user.first_name, self.athlete.user.last_name)

    class Meta:
        default_permissions = ()
