from django.db import models


class SandaWeightCategory(models.Model):
    categoryName = models.CharField(max_length=255, null=False, blank=False)
    isDuilian = models.BooleanField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now_add=True)
    explanation = models.CharField(max_length=255, null=True, blank=True)
    ageGroup = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        if self.explanation:
            return '%s %s' % (self.categoryName, self.explanation)
        else:
            return '%s' % (self.categoryName)
    #
    # class Meta:
    #     default_permissions = ()
