from django.db import models
from accounts.models import User
from django.utils import timezone

#TODO group or playlist that is invite only
#TODO tag only/ public groups
#TODO Mini admin for a pulic group


#Should groups take all types of listening history, and weight it diffrently, or just take one type from users
class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True, null=True)
    wiki_url = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='images/tag')
    def __str__(self):
        return f'{self.name}'                

class Group(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        related_name='owner',
        related_query_name='owner',
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        User,
        related_name='users'
        )
    tags = models.ManyToManyField(
        Tag, 
        related_name='group_tags', 
        )
    summary = models.CharField(max_length=800, blank=True, null=True)
    image = models.ImageField(upload_to='images/group')
    public = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name}'
    
class Artist(models.Model):
    name = models.CharField(max_length=500)
    tag = models.ManyToManyField(
        Tag,
        related_name='artist_tags',
        related_query_name='artist_tags',
        blank=True)
    popularity = models.IntegerField(blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    mbid = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/artist')
    spotify_id = models.CharField(max_length=128, blank=True, null=True)
    spotify_url= models.CharField(max_length=128, blank=True, null=True)     
    def __str__(self):
        return f'{self.name}'

class Album(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)    
    external_url = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/album')    
    mbid = models.CharField(max_length=128)
    spotify_id = models.CharField(max_length=128, blank=True, null=True)
    spotify_url= models.CharField(max_length=128, blank=True, null=True)    
    def __str__(self):
        return f'{self.name}'
     
    
class Track(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    external_url = models.CharField(max_length=500, blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/track')    
    artist = models.ForeignKey(
        Artist,
        related_name='track',
        related_query_name='track',
        on_delete=models.CASCADE
    )
    mbid = models.CharField(max_length=128)
    spotify_id = models.CharField(max_length=128, blank=True, null=True)
    spotify_url= models.CharField(max_length=128, blank=True, null=True)    
    def __str__(self):
        return f'{self.name}'
  
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
    def __str__(self):
        return f'{self.user} played {self.track} on {self.played_on}'

    