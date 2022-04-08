from django.contrib.auth.models import User
from django.db import models

from wushu.models.Federation import Federation
from wushu.models.Person import Person
from wushu.models.Communication import Communication


class Athlete(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE)
    ekg = models.FileField(upload_to='files/', null=True, blank=True, verbose_name='EKG')
    eeg = models.FileField(upload_to='files/', null=True, blank=True, verbose_name='EEG')

    def __str__(self):
        return '%s %s' % (self.person.name, self.person.surName)

    class Meta:
        ordering = ['pk']
