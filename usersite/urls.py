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
from core.views import catagory_api, post_api

from accounts.views import (login_view, logout_view, register_view)

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('category', catagory_api, basename='catagory_api')
router.register('post', post_api, basename='post_api')

# QURAN Support:
# use this to add dynamic arabic support --> https://alquran.cloud/api
# 1. anywhere on the website users can say something like [Q!2:255] or Q!2:255
# 2. Javascript will take this special case, take out '2:255'
# 3. fetch API request to http://api.alquran.cloud/v1/ayah/2:255
# 4. read the response, and 
# 5. write the arabic text replacing [Q!2:255]

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('admin/', admin.site.urls),
    path('dashboard/', TemplateView.as_view(template_name='admin_v2/admin_dashboard_v2.html'), name='admin_dashboard_v2'),
    
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),    
    path('faq_v1/', TemplateView.as_view(template_name='faq.html'), name='faq_v1'),
    path('faq/', TemplateView.as_view(template_name='faq_v2.html'), name='faq_v2'),
    path('media/', TemplateView.as_view(template_name='media.html'), name='media'),
    path('about/', TemplateView.as_view(template_name='about_us_v2.html'), name='about'),
    path('roadmap/', TemplateView.as_view(template_name='roadmap_v2.html'), name='roadmap'),
    path('contact_us/', TemplateView.as_view(template_name='contact_us.html'), name='contact'),
    
    # testing
    path('login_v2/', TemplateView.as_view(template_name='accounts/login_v2.html'), name='base_v2'),

    # Urls from Accounts. Login, Logout, Register
    path('login/',login_view, name='login' ),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)