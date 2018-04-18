from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from info.views import index, track_get_recent_users, group_detail, user_all_tracks, user_all_track_history, user_recent_track_history, test, update_group_history, group_get_common_tracks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', index, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('user_all_tracks', user_all_tracks, name='user_all_tracks'),
    path('user_all_track_history', user_all_track_history, name ='user_all_track_history'),
    path('user_recent_track_history', user_recent_track_history, name ='user_recent_track_history'),
    path('test', test, name='test'),
    path('update_group_history', update_group_history, name='update_group_history'),
    path('group/<str:pk>', group_detail, name='group_detail'),
    path('group/<str:pk>/common_tracks', group_get_common_tracks, name='group_get_common_tracks'),
    path('track/get_recent_users/<int:pk>', track_get_recent_users, name= "track_get_recent_users"),  
]