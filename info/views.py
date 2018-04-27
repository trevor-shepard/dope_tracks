import operator
from datetime import timezone as tz
from datetime import datetime, timedelta
from operator import itemgetter
from collections import Counter
from functools import reduce

import requests
from django.db import transaction
from django.db.models import Q, QuerySet, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import dateformat, timezone

from core.utils import build_lastfm_api_call, spotify_api_search
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import GroupForm
from .models import Album, Artist, Group, Tag, Track, User, UserTrackHistory
from .serializers import GroupSerializer, TrackSerializer, UserSerializer, UserTrackHistorySerializer

#TODO view for user-read-currently-playing
#TODO integrate spotify api to get spotify url for song
# Stupid simple view to render login.



def index(request):
  return render(request, 'info/index.html')
#TODO filter search by primary key of last pulled class


@api_view(['GET'])
def get_global_top_plays(request):
  days = int(request.GET.get('days', 30))
  start = timezone.now() - timedelta(days=days)  
  history = UserTrackHistory.objects.filter(played_on__gte=start)
  history = history.values_list('track', flat=True)
  counts = Counter(history)
  top_tracks = counts.most_common(10)
  top_tracks = [Track.objects.get(id=track_id) for track_id, play_count in top_tracks] 
  tracks = TrackSerializer(top_tracks, many=True)
  return Response(tracks.data)
  

def get_global_most_common_tracks(request):
  days = int(request.GET.get('days', 30))
  start = timezone.now() - timedelta(days=days)  
  group = Users.objects.all()
  start = timezone.now() - timedelta(days=days)
  users = [Q(user=user) for user in group]
  for user in group.users.all():
    user_recent_track_history(user)
  history = UserTrackHistory.objects.filter(reduce(operator.or_, users), played_on__gte =start).order_by('-played_on')
  history = set(history.values_list('track', 'user'))
  counts = Counter(map(lambda x: x[0], history))
  top_tracks = counts.most_common(10)
  top_tracks = [Track.objects.get(id=track_id) for track_id, play_count in top_tracks]
  
  tracks = TrackSerializer(top_tracks, many=True)
  return Response(tracks.data)





#GROUP DISPLAY VIEWS
def group_detail(request, pk):
  group = get_object_or_404(Group, pk=pk)
  members = group.users.all()
  return render(request, 'info/group_detail.html', {'group':group, 'members': members})


@api_view(['GET'])
def group_get_common_tracks(request, pk):
  days = int(request.GET.get('days', 30))
  group = get_object_or_404(Group, pk=pk)
  start = timezone.now() - timedelta(days=days)
  users = [Q(user=user) for user in group.users.all()]
  for user in group.users.all():
    user_recent_track_history(user)
  history = UserTrackHistory.objects.filter(reduce(operator.or_, users), played_on__gte =start).order_by('-played_on')
  history = set(history.values_list('track', 'user'))
  counts = Counter(map(lambda x: x[0], history))
  top_tracks = counts.most_common(10)
  top_tracks = [Track.objects.get(id=track_id) for track_id, play_count in top_tracks]
  
  tracks = TrackSerializer(top_tracks, many=True)
  return Response(tracks.data)

def group_create(request):
  if request.method == "POST":
    form = GroupForm(request.POST)
    if form.is_valid():
      group= form.save(commit=False)
      group.owner = request.user
      group.save()
      group.users.set(form.cleaned_data['users'])
      group.tags.set(form.cleaned_data['tags'])
      return redirect('group_detail', pk=group.pk)

  else:
    form = GroupForm()
  return render(request, 'info/group_create.html', {'form': form})
  


#LASTFM API CALL VIEWS
def user_all_track_history(request):
  request.user = User.objects.get(username='narks28')
  _from = timezone.now() - timedelta(days=90)
  response = requests.get(build_lastfm_api_call(user=request.user, method='user.getRecentTracks', _from=_from))
  response.raise_for_status()
  initial_data = response.json()
  pull_tracks_and_artists(request.user, initial_data['recenttracks']['track'])
  page = 1

  while page <= int(initial_data['recenttracks']['@attr']['totalPages']):
    print(page)
    response = requests.get(build_lastfm_api_call(user=request.user, method='user.getRecentTracks', page=page))
    response.raise_for_status()
    data = response.json()
    pull_tracks_and_artists(request.user, data['recenttracks']['track'])
    page += 1
  request.user.last_track_pull = timezone.now()
  return JsonResponse({'page_count':page, 'inital_data': initial_data})
  
@transaction.atomic
def user_recent_track_history(user):
  start = dateformat.format(user.last_track_pull, 'U')
  now = dateformat.format(timezone.now(), 'U')
  response = requests.get(build_lastfm_api_call(user=user,_from=start, to=now, method='user.getRecentTracks'))
  response.raise_for_status()
  initial_data = response.json()
  pull_tracks_and_artists(user, initial_data['recenttracks']['track'])
  page = 1

  while page <= int(initial_data['recenttracks']['@attr']['totalPages']):
    response = requests.get(build_lastfm_api_call(user=user,_from=start, to=now, method='user.getRecentTracks', page=page))
    response.raise_for_status()
    data = response.json()
    pull_tracks_and_artists(user, data['recenttracks']['track'])
    page += 1
  user.last_track_pull = timezone.now()
  user.save() 

@transaction.atomic
def pull_tracks_and_artists(user, tracks):
  track_count = 0
  for track_json in tracks:
    track_count += 1
    
    artist, artist_created = Artist.objects.get_or_create(name=track_json['artist']['#text'], mbid=track_json['artist']['mbid'])
    track, track_created = Track.objects.get_or_create(name=track_json['name'], artist=artist)
    
    if artist_created:
      get_artist_tag(artist)

    if '@attr' in track_json.keys():
      track_datetime = timezone.now()
    else:
      track_datetime = datetime.fromtimestamp(int(track_json['date']['uts']), tz.utc)  
    record = UserTrackHistory(user=user, track=track, played_on=track_datetime)
    record.save()






#TRACK VIEWS
def track_info(request):
  #needs mbid or artist name AND track name
  response = requests.get(build_lastfm_api_call(mbid=request.mbid, method='track.getInfo'))
  response.raise_for_status()
  
  return JsonResponse(response.json())

@api_view(['GET'])
def track_get_recent_users(request, pk):
  days = int(request.GET.get('days', 30))
  group_pk = request.GET.get('group')
  
  track = get_object_or_404(Track, pk=pk)
  histories = UserTrackHistory.objects.filter(track=track, played_on__gte= timezone.now() - timedelta(days=days))
  
  users = histories.values_list('user', flat=True).distinct()
  users = [User.objects.get(pk=id) for id in users]
  
  if group_pk:
    group = get_object_or_404(Group, pk=group_pk)
    users = [user for user in users if group in user.squads.all()]
  
  users = UserSerializer(users, many=True)
  return Response(users.data)






#USER VIEWS
def user_all_tracks(user):
  response = requests.get(build_lastfm_api_call(user=user, method='user.getTopTracks', period='overall'))
  response.raise_for_status()
  data = response.json()
  tracks = []
  for track in data['toptracks']['track']:
    tracks.append(track)
  page = 1
  while page <= int(data['toptracks']['@attr']['totalPages']):
    response = requests.get(build_lastfm_api_call(user=user, method='user.getTopTracks', period='overall', page=page))
    response.raise_for_status()
    data = response.json()
    for track in data['toptracks']['track']:
      tracks.append(track)
    page += 1
  return JsonResponse(response.json())

def check_lastfm_user(request, user):
  response = requests.get(build_lastfm_api_call(user=user, method='user.getRecentTracks'))
  response.raise_for_status()
  return JsonResponse(response.json())

def user_detail(request, username):
  user = get_object_or_404(User, username=username)
  user_recent_track_history(user)
  return render(request, 'info/user_detail.html', {'user':user})

@api_view(['GET'])
def display_user_top_tracks(request, username):
  days = int(request.GET.get('days', 30))
  start = timezone.now() - timedelta(days=days)  
  user = get_object_or_404(User, username=username)
  history = UserTrackHistory.objects.filter(user=user, played_on__gte =start).order_by('-played_on')
  history = history.values_list('track', flat=True)
  count = Counter(history)
  top_20 = count.most_common(10)
  top_20 = [(Track.objects.get(id=track_id), playcount) for track_id, playcount in top_20]
  top_20 = [{'track':TrackSerializer(track).data, 'playcount': playcount} for track, playcount in top_20]
  return Response(top_20)
 

@api_view(['GET'])
def user_artist_when_played(request, username, artist):
  user = get_object_or_404(User, username=username)
  artist = get_object_or_404(Artist, name=artist)
  histories = UserTrackHistory.objects.filter(user=user, track__artist=artist) #add time params here
  tracks = UserTrackHistorySerializer(histories, many=True)
  return Response(tracks.data)

@api_view(['GET'])
def get_user_group_list(request, username):
  user = get_object_or_404(User, username=username)
  groups = user.squads.all()
  groups = GroupSerializer(groups, many=True)
  return Response(groups.data)

def user_group_list(request, username):
  return render(request, 'info/group_list.html')

#TODO compares user listening histories between users and returns commonalities integergr
def find_similar_user(request, username):
  days = int(request.GET.get('days', 30))
  start = timezone.now() - timedelta(days=days)
  user = get_object_or_404(User, username=username)
  users = User.objects.all().exclude(username=username).exclude(username = 'admin')
  user_history = UserTrackHistory.objects.filter(user=user, played_on__gte=start)
  users_history = [UserTrackHistory.objects.filter(user=user, played_on__gte=start) for user in users]
  import pdb; pdb.set_trace()







#TAG VIEWS
def get_artist_tag(artist):
  response = requests.get(build_lastfm_api_call(method='artist.getInfo', artist=artist.name))
  response.raise_for_status()
  artist, _ = Artist.objects.get_or_create(name=artist.name)
  data = response.json()

  if data.get('artist'):
    tags = data['artist']['tags']['tag']
    for _tag in tags:
      tag, _ = Tag.objects.get_or_create(name=_tag['name'], wiki_url=_tag['url'])
      if Artist.objects.filter(tag=tag).exists():
        artist.tag.add(tag)

def tag_info(request):
  response = requests.get(build_lastfm_api_call(tag=request.tag, method='tag.getInfo'))
  response.raise_for_status()
  return JsonResponse(response.json())

#TODO
@api_view(['GET'])  
def get_user_top_tags(request, username):
  days = int(request.GET.get('days', 30))
  start = timezone.now() - timedelta(days=days)
  user = get_object_or_404(User, username=username)
  history = UserTrackHistory.objects.filter(user=user, played_on__gte=start)
  tags = [listen.track.artist.tag.all() for listen in history]
  tags = [tag for tag in tags]
  import pdb; pdb.set_trace()



