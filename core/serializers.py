from rest_framework import serializers
from .models import catagories, Post, quran

class CatagorySerializer(serializers.ModelSerializer):
	class Meta:
		model = catagories
		fields = ( 'id', 'catagory_name', 'description')

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'title', 'link', 'detail', 'catagory', 'publish')

class QuranSerializer(serializers.ModelSerializer):
	class Meta:
		model = quran
		fields = ('request', 'aiyath_number', 'text', 'audio_64', 'audio_128', 'surah_number', 'surah_name', 'surah_englishName', 'surah_englishNameTranslation', 'surah_numberOfAyahs', 'surah_revelationType', 'numberInSurah', 'juz', 'manzil', 'page', 'ruku', 'hizbQuarter', 'sajda')

 
