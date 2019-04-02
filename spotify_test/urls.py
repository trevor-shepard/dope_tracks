from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from info.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('api/', include('info.urls')),
    path('', index, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('accounts.urls')),
]