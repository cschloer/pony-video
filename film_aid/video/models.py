from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title + ' - ' + self.url


class Note(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    ts = models.IntegerField()
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    POINT_START = 'PS'
    DEFENSE = 'DF'
    TURNOVER = 'TO'
    OTHER = 'OT'

    NOTE_TYPE = (
        (POINT_START, 'Start of Point'),
        (DEFENSE, 'Defensive Stop'),
        (TURNOVER, 'Offensive Turnover'),
        (OTHER, 'Other'),
    )
    note_type = models.CharField(
        max_length=2,
        choices=NOTE_TYPE,
        default=POINT_START,
    )

    def __str__(self):
        return self.title + ' - ' + str(self.video) + ' - ' + str(self.ts)
