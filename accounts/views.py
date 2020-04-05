from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.urls import reverse

from django.conf import settings

def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		# change redirect to profile page
		return redirect(reverse('core:new_blog'))
	context = {
		'title' : 'Please Log in',
		'sub_title' : 'Please enter your credentials',
		'button_text' : 'Login',
		'production' : settings.PRODUCTION,
		"form" : form,
	}
	return render(request, 'accounts/login.html', context)

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
		return redirect(reverse('core:new_blog'))
	context = {
		'title' : 'Register New Account',
		'sub_title' : 'Welcome to the community. Please fill the form to create your account',
		'button_text' : 'Register',
		'production' : settings.PRODUCTION,	
		"form":form,
	}
	return render(request, 'accounts/login.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')