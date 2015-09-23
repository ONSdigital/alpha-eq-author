from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=120)
    survey_id = models.CharField(max_length=10)

    def __unicode__(self):
        return self.title

