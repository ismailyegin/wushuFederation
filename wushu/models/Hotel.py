from django.db import models

from wushu.models import Federation
from wushu.models.Person import Person


class Hotel(models.Model):
    SINGLEROOM = 0
    DOUBLEROOM = 1

    HOTELTYPE = (
        (SINGLEROOM, 'SINGLE ROOM-81€'),
        (DOUBLEROOM, 'DOUBLE ROOM-63€'),

    )
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    registerStartDate = models.DateTimeField()
    registerFinishDate = models.DateTimeField()
    name = models.CharField(max_length=128, verbose_name='Hotel Room-Price', choices=HOTELTYPE)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE)
    totalDay = models.CharField(max_length=10, blank=True, null=True, verbose_name='Total Day')
    price = models.CharField(max_length=10, blank=True, null=True, verbose_name='Price')

    def __str__(self):
        return '%s %s' % (self.person.name, self.person.surName)

    class Meta:
        default_permissions = ()
