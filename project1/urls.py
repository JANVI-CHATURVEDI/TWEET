"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet/', include('tweet.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    
    path("__reload__/", include("django_browser_reload.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# path('accounts/', include('django.contrib.auth.urls'))  

# - Adds all built-in Django auth URLs under /accounts/:  
#   /login/, /logout/, /password_change/, /password_reset/, /reset/...  

# - Benefits:  
#   • No need to write auth views yourself  
#   • Secure and quick setup  
#   • Fully customizable by overriding templates in templates/registration/  

# - Example:  
#   Visiting /accounts/login/ → looks for templates/registration/login.html  
#   (uses Django’s default if you don’t provide one)
