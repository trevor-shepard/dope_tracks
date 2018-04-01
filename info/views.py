import requests
from django.http import JsonResponse
from django.shortcuts import render

from core.decorators import spotify_view


# Stupid simple view to render login.
def index(request):
  return render(request, 'info/index.html')


# Gets top tracks back as JSON for Medium Time Trange.
@spotify_view
def top_tracks(request, token):
  resp = requests.get(
    'https://api.spotify.com/v1/me/top/tracks',
    headers={
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {token}'
    }
  )
  resp.raise_for_status()

  return JsonResponse({
    'data': resp.json()
  })


# Gets top artists back as JSON for Medium Time Trange.
@spotify_view
def top_artists(request, token):
  resp = requests.get(
    'https://api.spotify.com/v1/me/top/artists',
    headers={
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {token}'
    }
  )
  resp.raise_for_status()

  return JsonResponse({
    'data': resp.json()
  })
