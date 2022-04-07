from django.db import models

from wushu.models import Federation
from wushu.models.Person import Person
from django.contrib.auth.models import User


class Officer(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE)


    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

