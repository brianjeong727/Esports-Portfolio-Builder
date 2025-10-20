from django.db import models

# Create your models here.


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
