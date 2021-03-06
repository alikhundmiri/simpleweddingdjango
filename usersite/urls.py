"""usersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core.views import post_api, quran_api#, catagory_api
from core.api.views import QuranAPIView

from accounts.views import (login_view, logout_view, register_view, telegram_bot)

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

router.register('post', post_api, basename='post_api')
router.register('quran', quran_api, basename='quran_api')

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    
    # VISITOR INTERFACE
    path('quran/', include('core.api.urls', namespace='quran-view')),
    # path('quran/<slug:slug>/', QuranAPIView.as_view(), name='quran-view'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),    
    
    path('faq_v1/', TemplateView.as_view(template_name='faq.html'), name='faq_v1'),
    path('faq/', TemplateView.as_view(template_name='faq_v2.html'), name='faq_v2'),
    path('media/', TemplateView.as_view(template_name='media.html'), name='media'),
    path('about/', TemplateView.as_view(template_name='about_us_v2.html'), name='about'),
    path('roadmap/', TemplateView.as_view(template_name='roadmap_v2.html'), name='roadmap'),
    path('contact_us/', TemplateView.as_view(template_name='contact_us.html'), name='contact'),
    
    # testing
    # path('login_v2/', TemplateView.as_view(template_name='accounts/login_v2.html'), name='base_v2'),

    # ADMIN INTERFACE
    path('login/',login_view, name='login' ),    
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('admin/', admin.site.urls),

    path('dashboard/', include('accounts.urls', namespace='dashboard')),

    # TELEGRAM BOT
    path('tbot/', telegram_bot, name='telegram_bot'),    

    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)