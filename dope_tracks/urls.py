from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from info import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),

    path('', views.index, name='index'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('accounts.urls')),

    path('user_all_tracks', views.user_all_tracks, name='user_all_tracks'),
    path('user_all_track_history', views.user_all_track_history, name ='user_all_track_history'),
    path('user_recent_track_history', views.user_recent_track_history, name ='user_recent_track_history'),


    path('group/<str:pk>', views.group_detail, name='group_detail'),
    path('group/<str:pk>/common_tracks', views.group_get_common_tracks, name='group_get_common_tracks'),
    path('group_create', views.group_create, name='group_create'),

    path('track/get_recent_users/<int:pk>', views.track_get_recent_users, name= "track_get_recent_users"),  
    path('check_lastfm_user/<str:user>', views.check_lastfm_user, name="check_lastfm_user"),
    
    path('user/top_tracks/<str:username>', views.display_user_top_tracks, name='display_user_top_tracks'),
    path('user/artist_when_played/<str:username>/<str:artist>', views.user_artist_when_played, name="user_artist_when_played"), 
    path('user/<str:username>', views.user_detail, name="user_detail"),
    
    path('user/group_list/<str:username>', views.user_group_list, name="user_groups_list"),
    path('user/get_group_list/<str:username>', views.get_user_group_list, name="get_user_group_list"),


    path('user/top_tags/<str:username>', views.get_user_top_tags, name='user_top_tags'),
    path('user/find_similar/<str:username>', views.find_similar_user, name="find_similar"),

    path('global/top_plays', views.get_global_top_plays, name="global_top_plays"),
    path('global/common_plays', views.get_global_most_common_tracks, name='global_common_tracks'),
    path('global', views.global_detail, name="global_detail"),

    path('test_get_artist_tag/<int:pk>', views.test_get_artist_tag, name="test"),

    path('spotify_callback', views.spotify_callback, name="spotify_callback"),
    

]   

