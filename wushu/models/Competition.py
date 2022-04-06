from django.db import models

from wushu.models.EnumFields import EnumFields
from wushu.models.CompetitionCategori import CompetitionCategori


class Competition(models.Model):
    OPEN = 'Pre-Registration Open'
    CLOSED = 'Pre-Registration Completed'
    WAITED = 'On Standby'

    STATUS_CHOICES = (
        (OPEN, 'Pre-Registration Open'),
        (CLOSED, 'Pre-Registration Completed'),
        (WAITED, 'On Standby')
    )

    INTERNATIONAL = 'International'
    INTERSCHOOL = 'Interschool'
    INTERUNIVERSITY = 'Inter-University'
    NATIONAL = 'National'

    COMPETITION_TYPE = (
        (INTERNATIONAL, 'International'),
        (INTERSCHOOL, 'Interschool'),
        (INTERUNIVERSITY, 'Inter-University'),
        (NATIONAL, 'National')
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    startDate = models.DateTimeField()

    finishDate = models.DateTimeField()
    location = models.CharField(blank=False, null=False, max_length=1000)
    branch = models.CharField(max_length=128, verbose_name='Branş', choices=EnumFields.BRANCH.value)
    subBranch = models.CharField(max_length=128, verbose_name='Alt Branş', choices=EnumFields.SUBBRANCH.value)
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    type = models.CharField(max_length=128, verbose_name='Türü', choices=COMPETITION_TYPE, default=NATIONAL)
    registerStartDate = models.DateTimeField(db_column='registerStartDate', blank=True,
                                             null=True)  # Field name made lowercase.
    registerFinishDate = models.DateTimeField(db_column='registerFinishDate', blank=True,
                                              null=True)  # Field name made lowercase.

    # catergori ekleme

    categori = models.ManyToManyField(CompetitionCategori)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
