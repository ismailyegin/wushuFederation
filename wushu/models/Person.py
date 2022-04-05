from django.db import models


class Person(models.Model):
    MALE = 'MAN'
    FEMALE = 'WOMAN'

    AB1 = 'AB Rh+'
    AB2 = 'AB Rh-'
    A1 = 'A Rh+'
    A2 = 'A Rh-'
    B1 = 'B Rh+'
    B2 = 'B Rh-'
    O1 = '0 Rh+'
    O2 = '0 Rh-'

    GENDER_CHOICES = (
        (MALE, 'MAN'),
        (FEMALE, 'WOMAN'),
    )

    BLOODTYPE = (
        (AB1, 'AB Rh+'),
        (AB2, 'AB Rh-'),
        (A1, 'A Rh+'),
        (A2, 'A Rh-'),
        (B1, 'B Rh+'),
        (B2, 'B Rh-'),
        (O1, '0 Rh+'),
        (O2, '0 Rh-'),

    )

    pasaport = models.CharField(max_length=120, null=True, blank=True)
    pasaportImage = models.ImageField(upload_to='pasaport/', null=True, blank=True, default='pasaport/user.png',
                                     verbose_name='pasaport Picture')
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profile Picture')

    birthDate = models.DateField(null=True, blank=True, verbose_name='Birth Date')
    gender = models.CharField(max_length=128, verbose_name='Gender', choices=GENDER_CHOICES, default=MALE)
    ekg = models.FileField(upload_to='files/', null=True, blank=True, verbose_name='EKG')
    eeg = models.FileField(upload_to='files/', null=True, blank=True, verbose_name='EEG')

    class Meta:
        default_permissions = ()

    def save(self, force_insert=False, force_update=False):
        if self.birthplace:
            self.birthplace = self.birthplace.upper()
        if self.motherName:
            self.motherName = self.motherName.upper()
        if self.motherName:
            self.fatherName = self.fatherName.upper()
        super(Person, self).save(force_insert, force_update)
