from django.urls import path
from . import views
from . import riot_views

urlpatterns = [
    path('profiles/', views.ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.ProfileRetrieveAPIView.as_view(), name='profile-detail'),
    # Riot proxy endpoints
    path('riot/lol/<str:region>/summoner/by-name/<str:summoner_name>/', riot_views.lol_summoner_by_name),
    path('riot/tft/<str:region>/summoner/by-name/<str:summoner_name>/', riot_views.tft_summoner_by_name),
    path('riot/valorant/<str:region>/account/by-puuid/<str:puuid>/', riot_views.valorant_account_by_puuid),
]
