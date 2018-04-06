import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone, dateformat
from datetime import timedelta

from core.utils import build_lastfm_api_call

#TODO view for user-read-currently-playing

# Stupid simple view to render login.
def index(request):
  return render(request, 'info/index.html')

def test(request):
  start = timezone.now() - timedelta(days=7)
  start = dateformat.format(start, 'U')
  response = requests.get(build_lastfm_api_call(user=request.user,_from=start, method='user.getRecentTracks'))
  response.raise_for_status()
  
  return JsonResponse(response.json())

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

