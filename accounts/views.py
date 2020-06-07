import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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

from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile, accountCode
from core.forms import ArticleForm, MetaTagForm, ReviewArticle, LinkForm, ReviewLink
from core.models import Post, catagories
from bots.telegram import send_message, send_pair_url, successful_connection, check_existing_user, check_existing_code, already_connnected, send_help, send_help_user, profile, coming_soon, please_pair
from django.contrib.auth.models import User


def login_view(request):
	key = request.GET.get('key')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		# change redirect to profile page
		if key:
			return redirect(reverse('dashboard:connect_telegram') + '?key={}'.format(key))
		else:
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
		return redirect(reverse('dashboard:settings_profile_edit') + '?next=setup')
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

@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def user_settings(request):
	context = {
		'title' : 'Settings',
		'production' : settings.PRODUCTION,
	}
	return render(request, 'accounts/user_settings.html', context)

@user_passes_test(lambda u:u.is_authenticated, login_url=reverse_lazy('login'))
def settings_profile_edit(request):
	next_page = request.GET.get('next')

	existing_details = Profile.objects.get(user=request.user)
	form = ProfileForm(request.POST or None, instance=existing_details)	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# messages.success(request, "Successfully Created")
		if next_page == 'setup':
			return redirect(reverse('dashboard:new'))
		else:
			return redirect(reverse('dashboard:user_settings'))

	context = {
		'title' : 'Edit bio',
		'button_text' : 'Confirm',
		'blog_title' : 'Edit your profile details',
		'production' : settings.PRODUCTION,
		'form' : form,
	}
	return render(request, 'accounts/settings_editor.html', context)



# ------------ T E L E G R A M    B O T
@csrf_exempt
def telegram_bot(request):
	# print('recieve the message.')
	try:
		# print('trying to find json')
		json_message = json.loads(request.body)

	except json.decoder.JSONDecodeError as err:
		print("Found no Json. here's your page")
		return HttpResponse("looking for something? Well, it's not here.")
	
	# write the code here to use the following data from JSON Response
	sender_id		= json_message['message']['from'].get('id')
	update_id		= json_message.get('update_id')
	message_text	= json_message['message'].get('text')
	message_date	= json_message['message'].get('date')

	first_name		= json_message['message']['from'].get('first_name')
	last_name		= json_message['message']['from'].get('last_name')

	registered_user = check_existing_user(sender_id)
	requested_user = check_existing_code(sender_id)

	if message_text == '/start':
		reply = send_message('', message_text, '', sender_id)
	
	# pair telegram account to website account
	elif message_text == '/pair':
		if registered_user:
			reply = already_connnected(sender_id)
		else:
			reply = send_pair_url(sender_id)
	
	# view website account profile
	elif message_text == '/profile':
		if registered_user:
			reply = profile(sender_id)
		else:
			reply = please_pair(sender_id)
	
	# feature coming soon
	elif message_text == '/unpair' or '/mystatus' or '/editprofile':
		if registered_user:
			reply = coming_soon(sender_id)
		else:
			reply = please_pair(sender_id)
	
	# send help
	elif message_text == '/help':
		if registered_user:
			reply = send_help_user(sender_id)
		else:		
			reply = send_help(sender_id)
	
	else:
		reply = send_message("hey {} {}".format(first_name, last_name), message_text, message_date, sender_id)

	return JsonResponse(reply, safe=False)

def connect_telegram(request):
	# get the code from url
	verify_code = request.GET.get('key')
	# print(verify_code)	
	# using the code, get the connected chat_id
	try:
		chat_id = accountCode.objects.get(verify_code=verify_code).chat_id
	
		# get current user details
		user = User.objects.get(username=request.user)


		# update their profile to inclide chat_id
		user.profile.chat_id = chat_id
		# save
		user.save()

		successful_connection(chat_id)
		# get telegram chat_id connected to key from accounts.accountCode, using verify_code
		# if not empty. set the Profile.chat_id with this chat_id
		message = 'Your Simple wedding Account is now linked to this Telegram account.'
		status = True

	except accountCode.DoesNotExist:
		chat_id = None
		message = 'Connection failed. You will soon recieve a new link on telegram.'
		# alert Superuser.
		# send new link to connect
		status = False

	

	context = {
		'title' : 'Connecting to Telegram',
		'message' : message,
		'status' : status,
		'production' : settings.PRODUCTION,

	}

	return render(request, 'accounts/telegram_confirm.html', context)

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
	# print(slug)
	# print(post.slug)
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

# ------------ O T H E R     F U N C T I O N S

# TODO
# fall back for case where og:title and og:description are not used
def fetch_details_from_link(link):
	r = requests.get(link)
	soup = BeautifulSoup(r.text, features="lxml")	


	title = soup.title.string
	# check if link is of youtube
	# if youtube, description = 'youtube'
	# if youtube, detail = video_id
	o = urlparse(link)
	# if it is, then return different values
	# print(o.netloc)
	# print(type(o.netloc))
	youtube_urls = ["youtube.com", "www.youtube.com", "youtu.be"]
	if o.netloc not in youtube_urls: #<- netloc returns the domain name
		
		try:
			description = soup.find("meta",  property="og:description")["content"]
		except Exception as e:
			description = title
		
		detail = 'empty'

	else:
		description = 'youtube'
		# TODO: strip time stamp from video
		if o.query:
			detail = o.query.replace('v=','') #<-- https://www.youtube.com/watch?v=nxf41fMX_Y4 [v=nxf41fMX_Y4 ]
		else:
			detail = o.path.replace('/','') #<-- https://youtu.be/nxf41fMX_Y4 [/nxf41fMX_Y4]

	# print('description', description)
	# print('detail', detail)

	return title, description, detail

