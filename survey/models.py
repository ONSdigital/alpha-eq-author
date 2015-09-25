from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=120)
    survey_id = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.title


class Questionnaire(models.Model):
    questionnaire_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=120)
    overview = models.TextField(max_length=3000)
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    help_text = models.CharField(max_length=120)
    error_text = models.CharField(max_length=120)
    questionnaire = models.ForeignKey(Questionnaire)

    def __unicode__(self):
        return self.title

