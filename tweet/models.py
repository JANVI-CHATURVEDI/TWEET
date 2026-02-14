from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
import re


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('avatar', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.name}"        

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=280)
    photo = CloudinaryField('photo', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tweets_tag_set")
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
    
    # Override the save method to extract hashtags and associate them with the tweet
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Saves the Tweet in database ,Assigns it an ID 
        
        # save method keeps adding tags every time the tweet is saved 
        # If someone edits tweet text, old tags will still remain.
        # Clear old tags first
        self.tags.clear()
        
        # Find all hashtags
        hashtags = re.findall(r"#(\w+)", self.text) # have list of all hashtags in the text
        for tag_name in hashtags:
            tag, created = Tag.objects.get_or_create(name=tag_name.lower())
            self.tags.add(tag)    # Associate the tag with the tweet (ManyToMany relationship)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
    

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
