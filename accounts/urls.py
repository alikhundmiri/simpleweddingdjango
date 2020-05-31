"""insta2blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from . import views

app_name = "accounts"

urlpatterns = [
    # writer views
    path('', views.admin_dashboard, name='admin_dashboard'),
    # path('<str:username>', views.user_article, name='user_article'),
    path('new/', views.new, name='new'),
    path('new/blog/', views.new_blog, name='new_blog'),
    path('new/link/', views.new_link, name='new_link'),
    
    path('blog/<slug:slug>/add_meta', views.blog_meta_description, name='blog_meta_description'),

    # Admin views
    path('blog/review', views.review_list, name='review_list'),
    path('blog/<slug:slug>/edit', views.edit_blog, name='edit_blog'),
	path('blog/<slug:slug>/review', views.review, name='review_article'),

    # users
    # telegram
    path('connect_telegram', views.connect_telegram, name='connect_telegram'),

]
