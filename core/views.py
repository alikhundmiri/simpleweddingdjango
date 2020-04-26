from django.conf import settings
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

# importing views
from .models import Post, catagories
from .forms import BlogForm, MetaTagForm, ReviewForm

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
	return render(request, 'core/blog_detail.html', context)

# TODO
# Show all blog by user
# if request.user == username, then show even publish=true & false blogs.
def user_article(request, username=None):
	this_user=User.objects.filter(username=username)
	if this_user.exists():
		if username == request.user.username:
			article = Post.objects.filter(user__username=username)
		else:
			article = Post.objects.filter(publish=True, user__username=username)
		print(article)
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

@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
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
		# return HttpResponseRedirect(instance.get_absolute_url())
		return redirect(reverse('core:blog_meta_description', kwargs={'slug':instance.slug}))



	context = {
		'title' : 'Submit New Article',
		'button_text' : 'Submit For Review',
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'core/blog_editor.html', context)

# TODO
# DONE Test the page when unauthorised user tries to access this page
# DONE Add edit blog btn
# DONE Add edit meta btn
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def edit_blog(request, slug=None):
	post = Post.objects.get(slug=slug)
	if request.user==post.user or request.user.is_staff:# or not request.user.is_superuser:
		pass
	else:
		raise Http404

	form = BlogForm(request.POST or None, instance=post)
	if form.is_valid():
		instance = form.save(commit=False)
		if not request.user.is_staff: #turn blog as unpublished if the blog is edited by non-admin
			instance.publish=False
		instance.save()
		# messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {
		'title' : 'Edit Article',
		'button_text' : 'Submit For Review',
		'blog_title' : post.title,		
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'core/blog_editor.html', context)

# TODO:
# DONE Add url to meta description
# DONE Create FORM
# DONE Create a meta-editor page
# DONE After new_blog, redirect user to here.
# Add character count on form using JQuery or something
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def blog_meta_description(request, slug=None):
	if request.user.is_authenticated:# or not request.user.is_staff or not request.user.is_superuser:
		pass
	else:
		raise Http404
	post = Post.objects.get(slug=slug)

	form = MetaTagForm(request.POST or None, instance=post)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {
		'title' : 'Meta Description',
		'button_text' : 'Submit',
		'blog_title' : post.title,		
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'core/meta_editor.html', context)


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
	form = ReviewForm(request.POST or None, instance=article)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# messages.success(request, "Successfully Created")
		return redirect(reverse('core:review_list'))


	context = {
		'title' : 'Reviewing Article',
		'button_text' : 'Submit',	
		'production' : settings.PRODUCTION,
		'article' : article,
		'form' : form,
	}
	return render(request, 'core/blog_editor.html', context)

	