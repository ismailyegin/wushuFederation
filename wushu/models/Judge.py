from django.db import models

from wushu.models import Federation
from wushu.models.Person import Person
from wushu.models.Communication import Communication
from django.contrib.auth.models import User


class Judge(models.Model):
    ADAYHAKEM = 0
    HAKEM = 1


    COMPEVENTTYPE = (
        (ADAYHAKEM, 'CANDIDATE JUDGE'),
        (HAKEM, 'JUDGE'),

    )
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    category = models.IntegerField(null=True, blank=True, choices=COMPEVENTTYPE)
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE)
    weight=models.IntegerField(null=True,blank=True,verbose_name='Kilo')
    height=models.IntegerField(null=True,blank=True,verbose_name='Boy')
    is_national=models.BooleanField(null=True,blank=True,verbose_name='Ulusal Hakem mi?')
    shirtSize=models.CharField(max_length=250,null=True,blank=True,verbose_name='Üst Beden')
    pantSize=models.CharField(max_length=250,null=True,blank=True,verbose_name='Alt Beden')





    def __str__(self):
        return '%s %s' % (self.person.name, self.person.surName)

    class Meta:
        default_permissions = ()
