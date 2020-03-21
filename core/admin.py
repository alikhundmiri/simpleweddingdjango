from django.contrib import admin

from .models import Post, catagories
# Register your models here.


class Post_Admin(admin.ModelAdmin):
	list_display = ['title', 'user', 'publish', 'updated']
	list_filter = ['title', 'user', 'publish', 'updated']
	search_fields = ['title', 'user', 'publish', 'updated']

admin.site.register(Post, Post_Admin)
admin.site.register(catagories)