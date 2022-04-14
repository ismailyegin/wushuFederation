from django.db import models

from wushu.models import Federation
from wushu.models.Person import Person


class Hotel(models.Model):
    SINGLEROOM = 0
    DOUBLEROOM = 1

    HOTELTYPE = (
        (SINGLEROOM, 'SINGLE ROOM'),
        (DOUBLEROOM, 'DOUBLE ROOM'),

    )
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    registerStartDate = models.DateTimeField(auto_now_add=True)
    registerFinishDate = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128, verbose_name='Hotel Room-Price', choices=HOTELTYPE)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.person.name, self.person.surName)

    class Meta:
        default_permissions = ()
