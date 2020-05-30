import json
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.contrib.auth.decorators import user_passes_test

from django.conf import settings
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from .forms import UserLoginForm, UserRegisterForm
from core.forms import ArticleForm, MetaTagForm, ReviewArticle, LinkForm, ReviewLink
from core.models import Post, catagories
from bots.telegram import send_message

def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		# change redirect to profile page
		return redirect(reverse('dashboard:admin_dashboard'))
	context = {
		'title' : 'Please Log in',
		'sub_title' : 'Enter your credentials',
		'button_text' : 'Login',
		'production' : settings.PRODUCTION,
		"form" : form,
	}
	return render(request, 'accounts/login_v2.html', context)

def register_view(request):
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		# change redirect to profile page
		# return redirect("/")
		return redirect(reverse('dashboard:admin_dashboard'))
	context = {
		'title' : 'Register New Account',
		'sub_title' : 'Welcome to the community. Please fill the form to create your account',
		'button_text' : 'Register',
		'production' : settings.PRODUCTION,	
		"form":form,
	}
	return render(request, 'accounts/login_v2.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')

# ------------ T E L E G R A M    B O T
@csrf_exempt
def telegram_bot(request):
	print('recieve the message.')
	try:
		print('trying to find json')
		json_message = json.loads(request.body)

	except json.decoder.JSONDecodeError as err:
		print("Found no Json. here's your page")
		return HttpResponse("Welcome, Thanos! Sons of Alars")
	
	# write the code here to use the following data from JSON Response
	sender_id		= json_message['message']['from'].get('id')
	update_id		= json_message.get('update_id')
	message_text	= json_message['message'].get('text')
	message_date	= json_message['message'].get('date')

	first_name		= json_message['message']['from'].get('first_name')
	last_name		= json_message['message']['from'].get('last_name')

	message_body = message_text
	
	reply = send_message("hey {} {}".format(first_name, last_name), message_body, message_date, sender_id)
	return JsonResponse(reply)


# ------------ A D M I N    I N T E R F A C E     P A G E S 

# User admin Dashboard
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def admin_dashboard(request):
	article = Post.objects.filter(user__username=request.user.username)

	# get all blogs
	# get all topics
	# get all links

	context = {
		'production' : settings.PRODUCTION,
		'blogs' : article,
		# 'editable' : editable,
	}
	return render(request, 'accounts/admin_dashboard_v2.html', context)

# Choose what type of post you want to post
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def new(request):
	context = {
		'title' : 'Submit New Article',
		'button_text' : 'Submit For Review',
		'production' : settings.PRODUCTION,
	}
	return render(request, 'accounts/new.html', context)	


# Add new blog page
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def new_blog(request):
	form = ArticleForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# messages.success(request, "Successfully Created")
		# return HttpResponseRedirect(instance.get_absolute_url())
		return redirect(reverse('dashboard:blog_meta_description', kwargs={'slug':instance.slug}))



	context = {
		'title' : 'Submit New Article',
		'button_text' : 'Submit For Review',
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'accounts/blog_editor.html', context)


# Add new link page
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def new_link(request):

	form = LinkForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		link = instance.link

		# fetch the title
		# fetch the meta_description
		title, meta_description, link_detail = fetch_details_from_link(link)

		instance.title = title
		instance.meta_description = meta_description
		instance.detail = link_detail
		instance.save()
		# messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
		# return redirect(reverse('core:blog_meta_description', kwargs={'slug':instance.slug}))
		# return redirect(reverse('core:new_link'))

	context = {
		'title' : 'Submit New Link',
		'button_text' : 'Submit For Review',
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'accounts/new_link.html', context)	

# Edit blog page
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def edit_blog(request, slug=None):
	post = Post.objects.get(slug=slug)
	if request.user==post.user or request.user.is_staff:# or not request.user.is_superuser:
		pass
	else:
		raise Http404

	form = ArticleForm(request.POST or None, instance=post)
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
	return render(request, 'accounts/blog_editor.html', context)

# TODO
# DONE Add url to meta description
# DONE Create FORM
# DONE Create a meta-editor page
# DONE After new_blog, redirect user to here.
# Add character count on form using JQuery or something

# Add/Edit blog meta Description page
@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def blog_meta_description(request, slug=None):
	if request.user.is_authenticated:# or not request.user.is_staff or not request.user.is_superuser:
		pass
	else:
		raise Http404
	post = Post.objects.get(slug=slug)
	print(slug)
	print(post.slug)
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
		'blog_slug' : slug,	
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'accounts/meta_editor.html', context)

# @staff_member_required

# Review list page
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
	return render(request, 'accounts/review_list.html', context)

# @staff_member_required

# Review blog page
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def review(request, slug=None):
	article = get_object_or_404(Post, slug=slug)
	if article.link == '':
		form=ReviewArticle(request.POST or None, instance=article)
	else:
		form=ReviewLink(request.POST or None, instance=article)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.publish = True
		instance.save()
		# messages.success(request, "Successfully Created")
		return redirect(reverse('dashboard:review_list'))


	context = {
		'title' : 'Reviewing Article',
		'button_text' : 'Submit',	
		'production' : settings.PRODUCTION,
		'article' : article,
		'form' : form,
	}
	return render(request, 'accounts/blog_editor.html', context)

