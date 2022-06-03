"""postanything URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# This imports have to do with managing images
from django.conf import settings
from django.conf.urls.static import static
from users.views import register
from django.contrib.auth.views import LoginView, LogoutView
from users.views import login_view, update_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', view=register, name='register'),
    #path('login/', view=LoginView.as_view(template_name="users/login.html"), name='login'),
    path('login/', view=LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', view=LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('update_user/', view=update_user, name='update_user'),
]

# This conditional has to do with managing images, but just during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
