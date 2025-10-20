import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def lol_summoner_by_name(request, region, summoner_name):
    """Proxy to Riot's Summoner V4 endpoint by name."""
    api_key = settings.RIOT_API_KEY
    if not api_key:
        return Response({'detail': 'RIOT_API_KEY not configured on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)


@api_view(['GET'])
def tft_summoner_by_name(request, region, summoner_name):
    api_key = settings.RIOT_API_KEY
    if not api_key:
        return Response({'detail': 'RIOT_API_KEY not configured on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    url = f'https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)


@api_view(['GET'])
def valorant_account_by_puuid(request, region, puuid):
    api_key = settings.RIOT_API_KEY
    if not api_key:
        return Response({'detail': 'RIOT_API_KEY not configured on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Valorant uses different endpoints /valorant/v1 by region; this is a simple attempt
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
    headers = {'X-Riot-Token': api_key}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)
