from django.db import models

from wushu.models.Coach import Coach
from wushu.models.Competition import Competition


class SandaCoach(models.Model):

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.coach.person.name, self.coach.person.name)

    class Meta:
        default_permissions = ()
