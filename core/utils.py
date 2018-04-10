from django.conf import settings
import requests
import base64

def build_lastfm_api_call(**kwargs):
    query_params = '?'
    for key, value in kwargs.items():
        key = key.lstrip('_')
        query_params += f'{key}={value}&'
    query_params += f'api_key={settings.SOCIAL_AUTH_LASTFM_KEY}'

    return f'http://ws.audioscrobbler.com/2.0/{query_params}&format=json'

def get_spotify_api_token():
    base64_auth = base64.urlsafe_b64encode(f'{settings.SOCIAL_AUTH_SPOTIFY_KEY}:{settings.SOCIAL_AUTH_SPOTIFY_SECRET}'.encode()).decode()
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'client_credentials'      
        },
        headers={
            'Authorization': f'Basic {base64_auth}',
        }
    )
    response.raise_for_status()
    return response.json()['access_token']

def build_spotify_api_search_call(**kwargs):
    query_params = '?'
    for key, value in kwargs.items():
        key = key.lstrip('_')
        query_params += f'{key}={value}&'

    return f'https://api.spotify.com/v1/search{query_params}'

def spotify_api_search(**kwargs):
    token = get_spotify_api_token()
    url = build_spotify_api_search_call(**kwargs)
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})

    response.raise_for_status()

    return response.json()