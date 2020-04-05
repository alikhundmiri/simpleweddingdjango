from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.conf import settings

# importing views
from .models import Post, catagories

# rest framework stuff
from rest_framework import viewsets


from .serializers import CatagorySerializer, PostSerializer

class catagory_api(viewsets.ModelViewSet):
	queryset = catagories.objects.all()
	serializer_class = CatagorySerializer

class post_api(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer


def index(request):
	# import data from models
	links = Post.objects.filter(publish=True)

	context = {
		'production' : settings.PRODUCTION,
		'links' : links,
	}
	return render(request, 'core/blog_list.html', context)

def article(request, slug=None):
	# try:
	# use this as try and except once there is 404 page
	article = get_object_or_404(Post, slug=slug)
	# except Exception as e:
	# 	return render(request, 'error_404.html')

	context = {
		'production' : settings.PRODUCTION,
		'article' : article,
	}
	return render(request, 'core/blog_detail.html', context)