from django.conf import settings
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

# importing views
from .models import Post, catagories
from .forms import BlogForm

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
	if request.user.is_authenticated:
		article = get_object_or_404(Post, slug=slug)
	else:
		article = get_object_or_404(Post, slug=slug, publish=True)
	# except Exception as e:
	# 	return render(request, 'error_404.html')

	context = {
		'production' : settings.PRODUCTION,
		'article' : article,
	}
	return render(request, 'core/blog_detail.html', context)


def new_blog(request):
	if request.user.is_authenticated:# or not request.user.is_staff or not request.user.is_superuser:
		pass
	else:
		raise Http404
	form = BlogForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {
		'title' : 'Submit New Article',
		'button_text' : 'Submit For Review',
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'core/blog_editor.html', context)

# @staff_member_required
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def review_list(request):
	if request.user.is_staff:# or not request.user.is_staff or not request.user.is_superuser:
		pass
	else:
		raise Http404

	links = Post.objects.filter(publish=False)

	context = {
		'production' : settings.PRODUCTION,
		'links' : links,
	}
	return render(request, 'core/review_list.html', context)


# @staff_member_required
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def review(request, slug=None):
	article = get_object_or_404(Post, slug=slug)
	form = BlogForm(request.POST or None, instance=article)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.publish = True
		instance.save()
		# messages.success(request, "Successfully Created")
		return redirect(reverse('core:review_list'))


	context = {
		'title' : 'Reviewing Article',
		'button_text' : 'Publish',	
		'production' : settings.PRODUCTION,
		'article' : article,
		'form' : form,
	}
	return render(request, 'core/blog_editor.html', context)

	