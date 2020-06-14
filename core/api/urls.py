from .views import QuranAPIView
from django.urls import path, include
from django.conf import settings

# from rest_framework import routers
# from rest_framework.authtoken.views import obtain_auth_token

app_name = 'quran-api'

urlpatterns = [
	path('<slug:slug>/', QuranAPIView.as_view(), name='quran-view'),

]
