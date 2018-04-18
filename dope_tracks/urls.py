from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from info.views import index, user_all_tracks, user_all_track_history, user_recent_track_history, get_lindsey, test, group_detail, update_group_history

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', index, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('user_all_tracks', user_all_tracks, name='user_all_tracks'),
    path('user_all_track_history', user_all_track_history, name ='user_all_track_history'),
    path('user_recent_track_history', user_recent_track_history, name ='user_recent_track_history'),
    path('get_lindsey', get_lindsey, name ='get_lindsey'),
    path('test', test, name='test'),
    path('group_detail', group_detail, name='group_detail'),
    path('update_group_history', update_group_history, name='update_group_history'),
        
]