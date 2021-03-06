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

app_name = "core"

urlpatterns = [
    # user views 
    # path('', TemplateView.as_view(template_name='welcome.html'), name='index'),
    # path('', TemplateView.as_view(template_name='base_v2.html'), name='index'),
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.article, name='article'),
    
    # writer views
    path('user/<str:username>', views.user_article, name='user_article'),

    # Admin views
    # path('blog/review', views.review_list, name='review_list'),
    # path('blog/<slug:slug>/edit', views.edit_blog, name='edit_blog'),
	# path('blog/<slug:slug>/review', views.review, name='review_article'),

    # users

]
