from django.contrib.auth.models import User
from django.db import models

from wushu.models.Level import Level
from wushu.models.Communication import Communication
from wushu.models.Person import Person


class Coach(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, blank=True, null=True)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grades = models.ManyToManyField(Level, related_name='CoachGrades', blank=True, null=True)
    visa = models.ManyToManyField(Level, related_name='CoachVisa', blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ['pk']
        default_permissions = ()
