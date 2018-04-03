from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from info.views import index, top_tracks, top_artists

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', index, name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('top_tracks', top_tracks, name='top_tracks'),
    path('top_artists', top_artists, name='top_artists'),
    path('accounts/', include('accounts.urls')),
]