from django.db import models


class YearsTaoluCategory(models.Model):
    categoryYear = models.CharField(max_length=255, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now_add=True)
    explanation = models.CharField(max_length=255, null=True, blank=True)
    startYear = models.IntegerField(null=True, blank=True)
    finishYear = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.explanation:
            return '%s %s' % (self.categoryYear, self.explanation)
        else:
            return '%s' % (self.categoryYear)

    # class Meta:
    #     default_permissions = ()
