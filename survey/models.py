from django.db import models
import jsonfield


class Survey(models.Model):
    title = models.CharField(max_length=120)
    survey_id = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.title


class Questionnaire(models.Model):
    questionnaire_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=120)
    overview = models.TextField(max_length=3000)
    introduction_text = models.TextField(max_length=3000)
    survey = models.ForeignKey(Survey)
    reviewed = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    questionnaire_json = jsonfield.JSONField()

    def __unicode__(self):
        return self.title
