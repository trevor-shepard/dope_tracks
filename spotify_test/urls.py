from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from info.views import index, test, user_all_tracks, user_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', index, name='index'),
    path('detail/', user_detail, name='user_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('test', test, name='test'),
    path('user_all_tracks', user_all_tracks, name='user_all_tracks'),

]