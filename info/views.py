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

# Render Methods
def index(request):
  return render(request, 'info/index.html')


# API Endpoints


# api/top
def stats(request):
  user = get_object_or_404(User, pk=request.user.pk)

  if request.method == "GET":
    days = request.GET['start']
    

    history = UserTrackHistory.objects.filter(user=user).filter(played_on__gte=start)

    import pdb; pdb.set_trace()


# api/history
def history(request):
  user = get_object_or_404(User, pk=request.user.pk)

  if request.method == "GET":
    start = request.GET['start']
    response = requests.get(build_lastfm_api_call(user=request.user, method='user.getrecenttracks', limit='200', start=start))
    response.raise_for_status()
    data = response.json()
    tracks = []
    for track in data['recenttracks']['track']:
      tracks.append(track)
    page = 1
    while page <= int(data['recenttracks']['@attr']['totalPages']):
      response = requests.get(build_lastfm_api_call(user=request.user, method='user.getrecenttracks', limit='200', start=start, page=page))
      response.raise_for_status()
      data = response.json()
      for track in data['recenttracks']['track']:
        tracks.append(track)
      page += 1

    record_user_history(user, tracks)

      
    return JsonResponse(response.json())




# Private Methods
def record_user_history(user, tracks_data):
  for track_data in tracks_data:
    # check to see if mbid exists, use artist name if mbid does not exist as primary key
    if track_data['artist']['mbid'] == "":
      artist, artist_created = Artist.objects.get_or_create(
        mbid=track_data['artist']['#text']
      )
    else:
      artist, artist_created = Artist.objects.get_or_create(
        mbid=track_data['artist']['mbid']
      )

    # if new artist created, save to database
    if artist_created:
      artist.name = track_data['artist']['#text']
      artist.save()
      print(f'{artist.name} saved')

    # check to see if mbid exists, use track name if mbid does not exist as primary key
    if track_data['mbid'] == "":
      track, track_created = Track.objects.get_or_create(
        mbid=track_data['name']
      )
    else:
      track, track_created = Track.objects.get_or_create(
        mbid=track_data['mbid']
      )

    # if new track created, save to database
    if track_created:
      track.name = track_data['name']
      track.artist.add(artist)
      track.save()
      print(f"{track.name} saved")

    # create new listening event
    event = UserTrackHistory(
      user= user,
      track= track
    )
    event.save()
    print(f"{user.username} listening to {track.name} saved")
  
  # update user's last track pull to prevent pulling duplicate histories
  user.last_track_pull = timezone.now()
  user.save()
  print(f"user history updated at {timezone.now()}")
    
    

    












