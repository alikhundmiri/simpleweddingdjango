import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from django.conf import settings
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

# importing views
from .models import Post, catagories
from .forms import ArticleForm, MetaTagForm, ReviewArticle, LinkForm, ReviewLink

# rest framework stuff
from rest_framework import viewsets


from .serializers import CatagorySerializer, PostSerializer

class catagory_api(viewsets.ModelViewSet):
	queryset = catagories.objects.all()
	serializer_class = CatagorySerializer

class post_api(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

# ------------ V I S I T O R    I N T E R F A C E     P A G E S 

def index(request):
	blogs = Post.objects.filter(publish=True)[:5]

	context = {
		'production' : settings.PRODUCTION,
		'blogs': blogs,
	}
	return render(request, 'welcome_v2.html', context)

def blog(request):
	# import data from models
	links = Post.objects.filter(publish=True)

	context = {
		'production' : settings.PRODUCTION,
		'links' : links,
	}
	return render(request, 'core/blog_v2_list.html', context)

def article(request, slug=None):
	editable = False
	# try:
	# use this as try and except once there is 404 page
	if request.user.is_authenticated:
		article = get_object_or_404(Post, slug=slug)
	else:
		article = get_object_or_404(Post, slug=slug, publish=True)
	# except Exception as e:
	# 	return render(request, 'error_404.html')
	if request.user.is_authenticated:# or not request.user.is_staff or not request.user.is_superuser:
		if request.user==article.user or request.user.is_staff:
			editable = True

	context = {
		'production' : settings.PRODUCTION,
		'article' : article,
		'editable' : editable,
	}
	return render(request, 'core/blog_v2_detail.html', context)

# TODO
# DONE Show all blog by user
# DONE if request.user == username, then show even publish=true & false blogs.
def user_article(request, username=None):
	this_user=User.objects.filter(username=username)
	if this_user.exists():
		if username == request.user.username:
			article = Post.objects.filter(user__username=username)
		else:
			article = Post.objects.filter(publish=True, user__username=username)
		# print(article)
	else:
		return Http404

	# if request.user.is_authenticated:# or not request.user.is_staff or not request.user.is_superuser:
		# if request.user==article.user or request.user.is_staff:
			# editable = True

	context = {
		'production' : settings.PRODUCTION,
		'links' : article,
		# 'editable' : editable,
	}
	return render(request, 'core/blog_list.html', context)

# ------------ O T H E R     F U N C T I O N S

# TODO
# fall back for case where og:title and og:description are not used
def fetch_details_from_link(link):
	r = requests.get(link)
	soup = BeautifulSoup(r.text, features="lxml")	


	title = soup.find("meta",  property="og:title")["content"]
	# check if link is of youtube
	# if youtube, description = 'youtube'
	# if youtube, detail = video_id
	o = urlparse(link)
	# if it is, then return different values
	# print(o.netloc)
	if o.netloc == "youtube.com" or "www.youtube.com" or "youtu.be": #<- netloc returns the domain name
		description = 'youtube'

		if o.query:
			detail = o.query.replace('v=','') #<-- https://www.youtube.com/watch?v=nxf41fMX_Y4 [v=nxf41fMX_Y4 ]
		else:
			detail = o.path.replace('/','') #<-- https://youtu.be/nxf41fMX_Y4 [/nxf41fMX_Y4]

		# print("detail", detail)
	else:
		description = soup.find("meta",  property="og:description")["content"]
		detail = 'empty'

	return title, description, detail

