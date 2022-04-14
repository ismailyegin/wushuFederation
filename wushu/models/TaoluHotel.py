from django.db import models

from wushu.models.Hotel import Hotel
from wushu.models.Competition import Competition


class TaoluHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.hotel.person.name, self.hotel.person.surName)

    class Meta:
        default_permissions = ()
