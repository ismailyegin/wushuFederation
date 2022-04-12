from django.db import models

from wushu.models.Judge import Judge
from wushu.models.Competition import Competition


class TaoluJudge(models.Model):
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.judge.person.name, self.judge.person.surName)

    class Meta:
        default_permissions = ()
