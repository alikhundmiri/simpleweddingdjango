from django.contrib import admin

from .models import Post, catagories, quran
# Register your models here.


class Post_Admin(admin.ModelAdmin):
	list_display = ['title', 'user', 'publish', 'updated']
	list_filter = ['title', 'user', 'publish', 'updated']
	search_fields = ['title', 'user', 'publish', 'updated']


class Quran_Admin(admin.ModelAdmin):
	list_display = ['surah_englishName', 'numberInSurah', 'aiyath_number', 'request', 'updated']
	list_filter = ['surah_englishName', 'numberInSurah', 'aiyath_number', 'request', 'updated']
	search_fields = ['surah_englishName', 'numberInSurah', 'aiyath_number', 'request', 'updated']

admin.site.register(Post, Post_Admin)
admin.site.register(quran, Quran_Admin)
admin.site.register(catagories)