from rest_framework import serializers
from core.models import catagories, Post, quran

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
		fields = ('id', 'request', 'slug', 'aiyath_number', 'text', 'audio_64', 'audio_128', 'surah_number', 'surah_name', 'surah_englishName', 'surah_englishNameTranslation', 'surah_numberOfAyahs', 'surah_revelationType', 'numberInSurah', 'juz', 'manzil', 'page', 'ruku', 'hizbQuarter', 'sajda')
	# add code here to make this get_or_create
	# get using the ____ what?
	# def create(self, validated_data):
	# 	quran_, created = quran.objects.get_or_create(
	# 		slug=validated_data['slug'],
	# 		defaults={
	# 		'surah_number' : validated_data['surah_number'], 
	# 		'numberInSurah' : validated_data['numberInSurah'],
	# 		'aiyath_number': validated_data['aiyath_number'], 
	# 		'text': validated_data['text'], 
	# 		'audio_64': validated_data['audio_64'], 
	# 		'audio_128': validated_data['audio_128'], 
	# 		'surah_number': validated_data['surah_number'], 
	# 		'surah_name': validated_data['surah_name'], 
	# 		'surah_englishName': validated_data['surah_englishName'], 
	# 		'surah_englishNameTranslation': validated_data['surah_englishNameTranslation'], 
	# 		'surah_numberOfAyahs': validated_data['surah_numberOfAyahs'],
	# 		'surah_revelationType': validated_data['surah_revelationType'],
	# 		'numberInSurah': validated_data['numberInSurah'],
	# 		'juz': validated_data['juz'],
	# 		'manzil': validated_data['manzil'],
	# 		'page': validated_data['page'],
	# 		'ruku': validated_data['ruku'],
	# 		'hizbQuarter': validated_data['hizbQuarter'],
	# 		'sajda': validated_data['sajda']
	# 	})
	# 	return quran_


