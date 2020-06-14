from rest_framework import generics
from core.models import quran

from .serializers import QuranSerializer

class QuranAPIView(generics.RetrieveAPIView):
	lookup_field 			=	'slug'
	serializer_class 		=	QuranSerializer	
	queryset				=	quran.objects.all()

