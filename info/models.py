from django.db import models
from django.contrib.auth.models import User

#TODO add image fields to all models
#TODO find out what scope (token) needed to access artist info form href
#Should groups take all types of listening history, and weight it diffrently, or just take one type from users
class Group(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(
        User,
        related_name='groups',
        related_query_name='groups')

class Genre(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=400, blank=True, null=True)
    wiki_url = models.CharField(max_length=100, blank=True, null=True)

class Artist(models.Model):
    name = models.CharField(max_length=40)
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        related_query_name='genres')
    popularity = models.IntegerField(blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    spotify_id = models.CharField(
        max_length=30,
        primary_key=True,
        editable=False)   

class Album(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)    
    external_url = models.CharField(max_length=70, blank=True, null=True)
    uri = models.CharField(max_length=50)
    spotify_id = models.CharField(
        max_length=30,
        primary_key=True,
        editable=False)    
    
class Track(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    external_url = models.CharField(max_length=70, blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    uri = models.CharField(max_length=50)
    artist = models.ManyToManyField(Artist)
    spotify_id = models.CharField(
        max_length=30,
        primary_key=True,
        editable=False)    
    
#TODO pull listening history after last time pulled
#TODO
class UserTrackHistory(models.Model):
    user = models.ForeignKey(
        User,
        related_name='track_history',
        related_query_name='track_history',
        on_delete=models.CASCADE
        )

    TIME_RANGE = (
        ('S', 'Short'),
        ('M', 'Medium'),
        ('L', 'Long'),
        )
    time_range = models.CharField(max_length=1, choices=TIME_RANGE)
    date = models.DateTimeField(auto_now_add=True)
    tracks = models.ManyToManyField(
        Track
        related_name='track_history',
        related_query_name='track_history'
        )
    
class UserArtistHistory(models.Model):
    user = models.ForeignKey(
        User,
        related_name='artist_history',
        related_query_name='artist_history',
        on_delete=models.CASCADE
        )
    TIME_RANGE = (
        ('S', 'Short'),
        ('M', 'Medium'),
        ('L', 'Long'),
        )
    time_range = models.CharField(max_length=1, choices=TIME_RANGE)
    date = models.DateTimeField(auto_now_add=True)
    artists = models.ManyToManyField(
        Artist,
        related_name='artist_history',
        related_query_name='artist_history'
        )