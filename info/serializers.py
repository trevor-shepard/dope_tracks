from rest_framework import serializers
from .models import Group, Track, Artist
from accounts.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    class Meta:
        model = Track
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_track_pull']
