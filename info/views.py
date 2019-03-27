import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone, dateformat
from datetime import timedelta

from core.utils import build_lastfm_api_call

from accounts.models import User
from .models import Track, Album, UserTrackHistory, Tag, Artist


#TODO view for user-read-currently-playing



# refrence for structure of getrecenttracks
# {
# "artist": {
#   "mbid": "e2cf5b7b-63fa-4975-8b2d-bcefcd698ceb",
#   "#text": "Rodriguez Jr."
# },
# "album": {},
# "image": [],
# "streamable": "0",
# "date": {},
# "url": "https://www.last.fm/music/Rodriguez+Jr./_/Ellipsism",
# "name": "Ellipsism",
# "mbid": "e602b208-2312-4801-b346-348858673a17"
# }

# Stupid simple view to render login.
def index(request):
  return render(request, 'info/index.html')

def user_detail(request):
  return render(request, 'info/user_detail.html')

def lastfm_api_call(user, method, start):
  response = requests.get(build_lastfm_api_call(method='user.getRecentTracks', user=user, start=start, limit='200'))
  
    
  return response

def test(request):
  user = get_object_or_404(User, pk=request.user.pk)
  start = timezone.now() - timedelta(days=7)
  start = dateformat.format(start, 'U')
  response = lastfm_api_call(request.user, 'user.getrecenttracks', start)
  data = response.json()
  track_data = data['recenttracks']['track']
  record_user_history(user, track_data)
  
  return JsonResponse(response.json())



def user_all_tracks(request):
  user = get_object_or_404(User, pk=request.user.pk)
  
  response = requests.get(build_lastfm_api_call(user=request.user, method='user.getrecenttracks', limit='200'))
  response.raise_for_status()
  data = response.json()
  tracks = []
  # for track in data['toptracks']['track']:
  #   tracks.append(track)
  # page = 1
  # while page <= int(data['toptracks']['@attr']['totalPages']):
  #   response = requests.get(build_lastfm_api_call(user=request.user, method='user.getrecenttracks', limit='200', page=page))
  #   response.raise_for_status()
  #   data = response.json()
  #   for track in data['toptracks']['track']:
  #     tracks.append(track)
  #   page += 1

  # record_user_history(user, tracks)
    
  return JsonResponse(response.json())

def record_user_history(user, tracks_data):
  for track_data in tracks_data:
    artist, artist_created = Artist.objects.get_or_create(
      mbid=track_data['artist']['mbid']
    )

    if artist_created:
      artist.name = track_data['artist']['#text']
      artist.save()
      print(f'{artist.name} saved')


    track, track_created = Track.objects.get_or_create(
      mbid=track_data['mbid']
    )


    if track_created:
      track.name = track_data['name']
      track.artist.add(artist)
      track.save()
      print(f"{track.name} saved")

    event = UserTrackHistory(
      user= user,
      track= track
    )
    event.save()
    print(f"{user.username} listening to {track.name} saved")
    
    

    












