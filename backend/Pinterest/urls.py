"""Pinterest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
<<<<<<< HEAD
=======


#todo:front#3
>>>>>>> origin/dev
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),
<<<<<<< HEAD
<<<<<<< HEAD
    path('categories/', include('Categories.urls')),


=======

=======
    path('comments/', include('Comments.urls')),
>>>>>>> origin/dev
    path('categories/', include('Categories.urls')),
    path('pins/', include('Pins.api.v1.urls')),
    path('boards/', include('Boards.api.v1.urls')),
    path('chat/', include('Chat.urls')),
    path('pin/', include('Pins.urls')),
>>>>>>> 90fbf9f85c6fbc310f287a694229ace167505044
    path('', TemplateView.as_view(template_name='index.html'))



]
