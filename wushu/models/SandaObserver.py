from django.db import models

from wushu.models.Observer import Observer
from wushu.models.Competition import Competition


class SandaObserver(models.Model):

    observer = models.ForeignKey(Observer, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.observer.person.name, self.observer.person.name)

    class Meta:
        default_permissions = ()
