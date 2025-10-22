import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

RIOT_API_BASES = {
    "na1": "https://na1.api.riotgames.com",
    "euw1": "https://euw1.api.riotgames.com",
    "kr": "https://kr.api.riotgames.com",
    "americas": "https://americas.api.riotgames.com",
    "europe": "https://europe.api.riotgames.com",
    "asia": "https://asia.api.riotgames.com",
}

def riot_get(url):
    headers = {"X-Riot-Token": settings.RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    return Response(r.json(), status=r.status_code)

@api_view(["GET"])
def lol_summoner_by_name(request, region, summoner_name):
    base = RIOT_API_BASES.get(region, RIOT_API_BASES["na1"])
    url = f"{base}/lol/summoner/v4/summoners/by-name/{summoner_name}"
    return riot_get(url)

@api_view(["GET"])
def tft_summoner_by_name(request, region, summoner_name):
    base = RIOT_API_BASES.get(region, RIOT_API_BASES["na1"])
    url = f"{base}/tft/summoner/v1/summoners/by-name/{summoner_name}"
    return riot_get(url)

@api_view(["GET"])
def valorant_account_by_puuid(request, region, puuid):
    base = RIOT_API_BASES.get(region, RIOT_API_BASES["ap"])
    url = f"{base}/riot/account/v1/accounts/by-puuid/{puuid}"
    return riot_get(url)
