from django.conf import settings

def build_lastfm_api_call(**kwargs):
    query_params = '?'
    for key, value in kwargs.items():
        key = key.lstrip('_')
        print(key)
        query_params += f'{key}={value}&'
    query_params += f'api_key={settings.SOCIAL_AUTH_LASTFM_KEY}'

    return f'http://ws.audioscrobbler.com/2.0/{query_params}&format=json'