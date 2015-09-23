from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=120)
    survey_id = models.CharField(max_length=10)

    def __unicode__(self):
        return self.title


class Questionnaire(models.Model):
    questionnaire_id = models.CharField(max_length=10)
    title = models.CharField(max_length=120)
    overview = models.TextField(max_length=3000)
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return self.title
