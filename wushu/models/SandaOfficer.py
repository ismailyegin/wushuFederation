from django.db import models

from wushu.models.Officer import Officer
from wushu.models.Competition import Competition


class SandaOfficer(models.Model):

    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.officer.person.name, self.officer.person.name)

    class Meta:
        default_permissions = ()
