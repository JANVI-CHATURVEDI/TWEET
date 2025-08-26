from django.contrib import admin
from django.urls import path 
from . import views


urlpatterns = [
   
    
    path('', views.tweet_list, name='tweet_list'),
    path('tweet_create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('<int:pk>/', views.tweet_detail, name='tweet_detail'),
    path('<int:pk>/like/', views.like_tweet, name='like_tweet'),
    path('<int:pk>/repost/', views.repost_tweet, name='repost_tweet'),
    path('register/', views.register, name='register'),
]



# path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
# The <int:tweet_id> part is a placeholder in the URL.
# When you visit a URL like:
# http://127.0.0.1:8000/tweet/5/edit/

# Django matches it like this:
# 5 fits the <int:...> converter (so Django knows it’s an integer).
# Django assigns tweet_id = 5.
# Django calls your view:
# tweet_edit(request, tweet_id=5)
# Now inside tweet_edit, you can use tweet_id to look up that tweet in the database.


# How does the browser end up visiting /tweet/5/edit/?
# There are two main ways:
# 1. Manually typing the URL — not common for real apps.

# 2. Using {% url ... %} in templates:
# <a href="{% url 'tweet_edit' tweet_id=5 %}">Edit tweet</a>
# Django will automatically generate the URL /tweet/5/edit/.

