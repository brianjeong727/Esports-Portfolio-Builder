from django.db import models


class Profile(models.Model):
    """Stores a small set of user game/profile info for the portfolio demo."""
    display_name = models.CharField(max_length=100)
    game = models.CharField(max_length=100, blank=True)
    rank = models.CharField(max_length=50, blank=True)
    hours_played = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.display_name} ({self.game})"


# ---------------------------------------------------------------------
# RiotRSOToken model
# ---------------------------------------------------------------------
class RiotRSOToken(models.Model):
    """
    Stores OAuth tokens issued by Riot's Sign-On (RSO) system.
    Each record represents a single Riot user (identified by their 'sub' claim)
    and holds their access/refresh tokens for user-authorized API requests.
    """
    sub = models.CharField(max_length=200, unique=True)  # Riot account unique ID
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=1024, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    id_token = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RSO Token {self.sub}"
