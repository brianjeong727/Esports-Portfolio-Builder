from django.urls import path
from . import views, riot_views

urlpatterns = [
    path('profiles/', views.ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.ProfileRetrieveAPIView.as_view(), name='profile-detail'),

    # Riot API proxy endpoints (server-side using your developer key)
    path('riot/lol/<str:region>/summoner/by-name/<str:summoner_name>/', riot_views.lol_summoner_by_name),
    path('riot/tft/<str:region>/summoner/by-name/<str:summoner_name>/', riot_views.tft_summoner_by_name),
    path('riot/valorant/<str:region>/account/by-puuid/<str:puuid>/', riot_views.valorant_account_by_puuid),

    # Riot Sign-On (RSO) OAuth endpoints (user-authorized)
    path('riot/oauth/login/', riot_views.riot_rso_login, name='riot-rso-login'),
    path('riot/oauth/callback/', riot_views.riot_rso_callback, name='riot-rso-callback'),
    path('riot/account/me/<str:sub>/<str:cluster>/', riot_views.riot_account_me, name='riot-account-me'),

    path('riot/oauth/login-debug/', riot_views.riot_rso_login_debug),

]
