from django.db import models
from django.utils import timezone
from datetime import timedelta
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
    last_used_id = models.IntegerField(default=0)
    locked_on = models.DateTimeField(null=True, default=None)
    locked_by = models.TextField(max_length=120 , null=True, default=None)

    @property
    def locked(self):
        self.check_locked_time()
        return self.locked_by is not None

    def is_locked(self, username):
        locked = False
        # if it's locked
        if self.locked_by and not self.locked_by == username:
            # check how long it's been locked for and unlock if necessary
            self.check_locked_time()
            # check if its still locked
            if self.locked_by:
                locked = True
        return locked

    def check_locked_time(self):
        time_now = timezone.now()
        locked_time = time_now - self.locked_on
        if locked_time > timedelta(minutes=30):
            self.unlock()

    def lock(self, username):
        self.locked_by = username
        self.locked_on = timezone.now()
        self.save()

    def unlock(self):
        self.locked_on = None
        self.locked_by = None
        self.save()

    def __unicode__(self):
        return self.title
