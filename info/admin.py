from django.contrib import admin
from .models import Album, Artist, Track, UserTrackHistory, Group, Tag
# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(UserTrackHistory)
admin.site.register(Group)
admin.site.register(Tag)
