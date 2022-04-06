from django.db import models

from wushu.models.Person import Person
from wushu.models.Communication import Communication
from django.contrib.auth.models import User


class Observer(models.Model):

    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


