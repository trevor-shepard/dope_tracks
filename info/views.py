import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone, dateformat
from datetime import timedelta, datetime
from datetime import timezone as tz
from django.db import transaction
from core.utils import build_lastfm_api_call, spotify_api_search

from .models import User, UserTrackHistory, Track, Artist, Album, Tag, Group

#TODO view for user-read-currently-playing
#TODO integrate spotify api to get spotify url for song


# Stupid simple view to render login.
def index(request):
  return render(request, 'info/index.html')
#TODO filter search by primary key of last pulled class

def test(request):
  x = spotify_api_search(q="enya", type='artist')
  return JsonResponse(x)


def pull_tracks_and_artists(request, tracks):
  track_count = 0
  for track_json in tracks:
    track_count += 1
    
    artist, _ = Artist.objects.get_or_create(name=track_json['artist']['#text'], mbid=track_json['artist']['mbid'])
    track, _ = Track.objects.get_or_create(name=track_json['name'], artist=artist)
  
    if '@attr' in track_json.keys():
      track_datetime = timezone.now()
    else:
      track_datetime = datetime.fromtimestamp(int(track_json['date']['uts']), tz.utc)  
    record = UserTrackHistory(user=request.user, track=track, played_on=track_datetime)
    record.save()

@transaction.atomic
def user_recent_track_history(request):
  start = dateformat.format(request.user.last_track_pull, 'U')
  now = dateformat.format(timezone.now(), 'U')
  response = requests.get(build_lastfm_api_call(user=request.user,_from=start, to=now, method='user.getRecentTracks'))
  response.raise_for_status()
  initial_data = response.json()
  pull_tracks_and_artists(request, initial_data['recenttracks']['track'])
  page = 1

  while page <= int(initial_data['recenttracks']['@attr']['totalPages']):
    response = requests.get(build_lastfm_api_call(user=requests.user,_from=start, to=now, method='user.getRecentTracks', page=page))
    response.raise_for_status()
    data = response.json()
    pull_tracks_and_artists(request, data['recenttracks']['track'])
    page += 1
  request.user.last_track_pull = timezone.now()

  return JsonResponse({'page_count':page, 'inital_data': initial_data})

def get_lindsey(request):
  response = requests.get(build_lastfm_api_call(user='sethjohnsonpdx', method='user.getRecentTracks'))
  response.raise_for_status()
  initial_data = response.json()
  return JsonResponse(initial_data)


@transaction.atomic
def user_all_track_history(request):
  response = requests.get(build_lastfm_api_call(user=request.user, method='user.getRecentTracks'))
  response.raise_for_status()
  initial_data = response.json()
  pull_tracks_and_artists(request, initial_data['recenttracks']['track'])
  page = 1

  while page <= int(initial_data['recenttracks']['@attr']['totalPages']):
    response = requests.get(build_lastfm_api_call(user=request.user, method='user.getRecentTracks', page=page))
    response.raise_for_status()
    data = response.json()
    pull_tracks_and_artists(request, data['recenttracks']['track'])
    page += 1
  request.user.last_track_pull = timezone.now()
  return JsonResponse({'page_count':page, 'inital_data': initial_data})
  

def tag_info(request):
  response = requests.get(build_lastfm_api_call(tag=request.tag, method='tag.getInfo'))
  response.raise_for_status()
  
  return JsonResponse(response.json())

def track_info(request):
  #needs mbid or artist name AND track name
  response = requests.get(build_lastfm_api_call(mbid=request.mbid, method='track.getInfo'))
  response.raise_for_status()
  
  return JsonResponse(response.json())

def user_all_tracks(request):
  response = requests.get(build_lastfm_api_call(user=request.user, method='user.getTopTracks', period='overall'))
  response.raise_for_status()
  data = response.json()
  tracks = []
  for track in data['toptracks']['track']:
    tracks.append(track)
  page = 1
  while page <= int(data['toptracks']['@attr']['totalPages']):
    response = requests.get(build_lastfm_api_call(user=request.user, method='user.getTopTracks', period='overall', page=page))
    response.raise_for_status()
    data = response.json()
    for track in data['toptracks']['track']:
      tracks.append(track)
    page += 1
  return JsonResponse(response.json())


# # Gets top artists back as JSON for Medium Time Trange.
# @spotify_view
# def top_artists(request, token):
#   resp = requests.get(
#     'https://api.spotify.com/v1/me/top/artists',
#     headers={
#       'Accept': 'application/json',
#       'Content-Type': 'application/json',
#       'Authorization': f'Bearer {token}'
#     }
#   )
#   resp.raise_for_status()

#   return JsonResponse({
#     'data': resp.json()
#   })

