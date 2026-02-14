from django import forms
from .models import Tweet, Comment, Like, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'What’s happening?',
                'class': 'w-full px-3 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2'
            }),
        
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                # safely set avatar on existing profile
                profile, created = Profile.objects.get_or_create(user=user)
                profile.avatar = avatar
                profile.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Add a comment...',
                'class': 'w-full px-3 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2'
            }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'website']