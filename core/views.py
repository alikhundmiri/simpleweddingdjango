from django.shortcuts import render
from django.conf import settings

# importing views
from .models import Post


def index(request):
	# import data from models
	links = Post.objects.filter(publish=True)

	context = {
		'production' : settings.PRODUCTION,
		'links' : links,
	}
	return render(request, 'index.html', context)
