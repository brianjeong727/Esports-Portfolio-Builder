from django.shortcuts import render
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer


# Simple DRF views for creating/listing profiles.
class ProfileListCreateAPIView(generics.ListCreateAPIView):
	queryset = Profile.objects.all().order_by('-created_at')
	serializer_class = ProfileSerializer

class ProfileRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

