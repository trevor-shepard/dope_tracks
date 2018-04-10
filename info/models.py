from django.db import models
from accounts.models import User
from django.utils import timezone

#TODO add image fields to all models
#TODO find out what scope (token) needed to access artist info form href
#TODO group or playlist that is invite only
#TODO tag only/ public groups
#TODO Mini admin for a pulic group


#Should groups take all types of listening history, and weight it diffrently, or just take one type from users


class Group(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(
        User)
    summary = models.CharField(max_length=800, blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=400, blank=True, null=True)
    wiki_url = models.CharField(max_length=100, blank=True, null=True)

class Artist(models.Model):
    name = models.CharField(max_length=40)
    tag = models.ManyToManyField(
        Tag,
        related_name='tags',
        related_query_name='tags',
        blank=True)
    popularity = models.IntegerField(blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    mbid = models.CharField(
        max_length=30,
        )
    def __str__(self):
        return f'{self.name}'

class Album(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)    
    external_url = models.CharField(max_length=70, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    mbid = models.CharField(
        max_length=30,
        )    
    
class Track(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    external_url = models.CharField(max_length=70, blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=50)
    artist = models.ForeignKey(
        Artist,
        related_name='track',
        related_query_name='track',
        on_delete=models.CASCADE
    )
    mbid = models.CharField(
        max_length=30,
        )  
    def __str__(self):
        return f'{self.name}'
  
    
#TODO pull listening history after last time pulled
#TODO
class UserTrackHistory(models.Model):
    user = models.ForeignKey(
        User,
        related_name='track_history',
        related_query_name='track_history',
        on_delete=models.CASCADE
        )
    track = models.ForeignKey(
        Track,
        related_name='user_track_history',
        related_query_name='user_track_history',
        on_delete=models.CASCADE
    )
    played_on = models.DateTimeField(default=timezone.now)
    