from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


#TODO view for displaying profile data (genre listened to, groups, top artists/tracks)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
