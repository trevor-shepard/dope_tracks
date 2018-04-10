from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from requests.exceptions import HTTPError
from social_django.utils import load_strategy
import base64

from django.conf import settings
import requests

def lastfm_view(function):
  @login_required
  def wrap(request, *args, **kwargs):
    social = request.user.social_auth.get(provider='lastfm')
    session_key = social.extra_data.get('session_key')
    api_key = settings.SOCIAL_AUTH_LASTFM_KEY
    api_secret = settings.SOCIAL_AUTH_LASTFM_SECRET
  
    signature = hashlib.md5(''.join(
      ('api_key', api_key, 'methodauth.getSession', secret)
    ).encode()).hexdigest()

    credentials = {
      'session_key': session_key,
      'api_key': api_key,
      'signature': signature
    }
    try:
      return function(request, credentials, *args, **kwargs)
    except HTTPError as e:
      print(f'Failed using token because of HTTPError: "{e}"')
      return redirect('logout')


  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap






