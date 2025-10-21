import requests
import datetime
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import RiotRSOToken


# ---------------------------------------------------------------------
# Riot API proxy endpoints (developer key–based)
# ---------------------------------------------------------------------
@api_view(['GET'])
def lol_summoner_by_name(request, region, summoner_name):
    """Proxy to Riot's Summoner V4 endpoint by name."""
    api_key = settings.RIOT_API_KEY
    if not api_key:
        return Response(
            {'detail': 'RIOT_API_KEY not configured on server'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)

@api_view(['GET'])
def riot_rso_login_debug(request):
    from urllib.parse import urlencode
    client_id = settings.RIOT_RSO_CLIENT_ID
    redirect_uri = settings.RIOT_RSO_REDIRECT_URI
    scope = request.GET.get('scope') or getattr(settings, 'RIOT_RSO_SCOPE', 'openid')
    state = request.GET.get('state', 'state')

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': state,
    }
    auth_url = 'https://auth.riotgames.com/authorize?' + urlencode(params)
    return Response({
        'auth_url': auth_url,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope
    })

@api_view(['GET'])
def tft_summoner_by_name(request, region, summoner_name):
    """Proxy to TFT summoner endpoint."""
    api_key = settings.RIOT_API_KEY
    if not api_key:
        return Response(
            {'detail': 'RIOT_API_KEY not configured on server'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    url = f'https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)


@api_view(['GET'])
def valorant_account_by_puuid(request, region, puuid):
    """Proxy to Valorant account endpoint by PUUID."""
    api_key = settings.RIOT_API_KEY
    if not api_key:
        return Response(
            {'detail': 'RIOT_API_KEY not configured on server'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
    headers = {'X-Riot-Token': api_key}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)


# ---------------------------------------------------------------------
# Riot Sign-On (RSO) OAuth endpoints
# ---------------------------------------------------------------------
@api_view(['GET'])
def riot_rso_login(request):
    """
    Redirects user to Riot's authorization page to start OAuth login.
    Riot will redirect back to your callback with an authorization code.
    """
    client_id = settings.RIOT_RSO_CLIENT_ID
    redirect_uri = settings.RIOT_RSO_REDIRECT_URI
    scope = request.GET.get('scope') or getattr(settings, 'RIOT_RSO_SCOPE', 'openid')
    state = request.GET.get('state', 'state')

    if not client_id or not redirect_uri:
        return Response({'detail': 'RSO client configuration missing'}, status=500)

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': state,
    }
    return redirect('https://auth.riotgames.com/authorize?' + urlencode(params))


@api_view(['GET'])
def riot_rso_callback(request):
    """
    Handles Riot's redirect, exchanges authorization code for access tokens,
    stores them in the RiotRSOToken model, and returns the Riot user ID (sub).
    """
    code = request.GET.get('code')
    if not code:
        return Response({'detail': 'Missing authorization code'}, status=400)

    token_url = 'https://auth.riotgames.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.RIOT_RSO_REDIRECT_URI,
        'client_id': settings.RIOT_RSO_CLIENT_ID,
        'client_secret': settings.RIOT_RSO_CLIENT_SECRET,
    }

    r = requests.post(token_url, data=data)
    if r.status_code != 200:
        return Response(r.json(), status=r.status_code)

    token_data = r.json()
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token', '')
    id_token = token_data.get('id_token', '')
    expires_in = token_data.get('expires_in')
    expires_at = timezone.now() + datetime.timedelta(seconds=expires_in) if expires_in else None

    # Fetch the Riot user's unique ID (sub)
    sub = None
    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo = requests.get('https://auth.riotgames.com/userinfo', headers=headers)
        if userinfo.status_code == 200:
            sub = userinfo.json().get('sub')

    if not sub:
        return Response({'detail': 'Failed to obtain user identifier'}, status=400)

    RiotRSOToken.objects.update_or_create(
        sub=sub,
        defaults={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_at': expires_at,
            'id_token': id_token,
        },
    )
    return Response({'detail': 'authorization_success', 'sub': sub})


@api_view(['GET'])
def riot_account_me(request, sub, cluster):
    """
    Retrieves the Riot user's account info using a stored RSO token.
    Automatically refreshes the token if it has expired.
    """
    try:
        token_obj = RiotRSOToken.objects.get(sub=sub)
    except RiotRSOToken.DoesNotExist:
        return Response({'detail': 'No token found for this user'}, status=404)

    # Refresh expired tokens
    if token_obj.expires_at and token_obj.expires_at <= timezone.now():
        if not token_obj.refresh_token:
            return Response({'detail': 'Token expired and no refresh token'}, status=401)

        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': token_obj.refresh_token,
            'client_id': settings.RIOT_RSO_CLIENT_ID,
            'client_secret': settings.RIOT_RSO_CLIENT_SECRET,
        }
        r = requests.post('https://auth.riotgames.com/oauth/token', data=refresh_data)
        if r.status_code != 200:
            return Response(r.json(), status=r.status_code)

        new_data = r.json()
        token_obj.access_token = new_data.get('access_token', token_obj.access_token)
        token_obj.refresh_token = new_data.get('refresh_token', token_obj.refresh_token)
        expires_in = new_data.get('expires_in')
        if expires_in:
            token_obj.expires_at = timezone.now() + datetime.timedelta(seconds=expires_in)
        token_obj.save()

    # Fetch account info using Riot's user-authorized endpoint
    headers = {'Authorization': f'Bearer {token_obj.access_token}'}
    account_url = f'https://{cluster}.api.riotgames.com/riot/account/v1/accounts/me'
    r = requests.get(account_url, headers=headers)
    return Response(r.json(), status=r.status_code)
