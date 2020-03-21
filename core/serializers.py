from rest_framework import serializers
from .models import catagories, Post

class CatagorySerializer(serializers.ModelSerializer):
	class Meta:
		model = catagories
		fields = ( 'id', 'catagory_name', 'description')

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'title', 'link', 'detail', 'catagory', 'publish')



