from django.db import models
from django.contrib.auth.models import User
# User model is the same one you see in Django’s admin panel under “Users.”
# When you create, edit, or delete users in the admin panel, you’re working with this same User table in the database (auth_user).

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
# user (inside Tweet) → a ForeignKey field pointing to a User.
# - In the database: just stores user’s id.
# - In code: behaves like a full User object.
    text = models.TextField(max_length=280)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add: Automatically sets the field to the current datetime only when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)
    # auto_now: Automatically sets the field to the current datetime every time the object is saved (updated).
    reposted_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reposts'
    )

    @property
    def photo_url(self):
       if self.photo and hasattr(self.photo, 'url'):
          return self.photo.url
       return None


    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
    
# __str__ tells Django how to display your object as text.
# Without it → you see Tweet object (1) in admin/shell.
# With it → you see something meaningful like "alice: This is my first t".
# It’s just for readability and easier debugging.



class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)