from django.shortcuts import render
from .models import Tweet , Like
from .forms import TweetForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm ,TweetForm, CommentForm
from django.contrib.auth import login
from django.db.models import Case, When, Value, IntegerField

# Note:
# request.user has currently logged-in user.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    search_query = request.GET.get('q', '').strip()  # Get search term
    tweets = Tweet.objects.all()

    if search_query:
        tweets = tweets.annotate(
            match_order=Case(
                # Exact match first
                When(user__username__iexact=search_query, then=Value(1)),
                # Partial match next
                When(user__username__icontains=search_query, then=Value(2)),
                # Everything else
                default=Value(3),
                output_field=IntegerField()
            )
        ).order_by('match_order', '-created_at')
    else:
        tweets = tweets.order_by('-created_at')

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'search_query': search_query
    })

@login_required
def tweet_create(request):
    # This means the form was submitted by the user.
    # When the user fills the form and clicks "Submit," the browser sends a POST request with the data.
    if request.method == 'POST':  
        form = TweetForm(request.POST, request.FILES) # We create a form instance with the submitted data (request.POST) and uploaded files (request.FILES).
        if form.is_valid(): # Check if the form is valid (all required fields, max lengths, etc.).
            tweet = form.save(commit=False) # Create a Tweet object but don't save it to the database yet.
            tweet.user = request.user  # Set the user field of tweet to the currently logged-in user
            tweet.save()
            return redirect('tweet_list') # Redirect to the tweet list page
    else:
    #  This means the form has not been submitted yet, usually when the page is first opened.
    # We just want to display an empty form to the user:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id , user=request.user)  # Tweet is your model. Every Tweet has a unique id (primary key). pk is just a shortcut for the primary key, so pk=tweet_id means “get the Tweet whose id equals tweet_id.

    # POST means the form was submitted (user clicked “Save” or “Update”).
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)  # request.POST → The form data submitted by the user.
        # request.FILES → Any uploaded files (like images).
        # instance=tweet → Important! This tells Django:
        # “I want to update this existing tweet, not create a new one.”
        if form.is_valid():
            form.save(commit=False)  # Save the updated tweet
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')  # Redirect to the tweet list page
    else:
        form = TweetForm(instance=tweet)  # When the user opens the edit page, the form is pre-filled with the existing tweet data.
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)  # Get the tweet to delete, ensuring it belongs to the current user.
    
    if request.method == 'POST':  # If the user confirms deletion (usually by clicking a "Delete" button).
        tweet.delete()  # Delete the tweet from the database.
        return redirect('tweet_list')  # Redirect to the tweet list page after deletion.
    
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


@login_required
def tweet_detail(request, pk):   # if you see we never made use of Commemt from models bcuz in Comment model we have use foreign key to tweet so we can access comments from tweet object itself using related_name comments defined in model too . bcuz of foreign key comment is attached to tweet  and it also know which tweet it belongs too.
    tweet = get_object_or_404(Tweet, pk=pk)
    comments = tweet.comments.all().order_by('-created_at')

    # Comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.tweet = tweet
            new_comment.user = request.user
            new_comment.save()
            return redirect('tweet_detail', pk=tweet.pk)
    else:
        form = CommentForm()

    context = {
        'tweet': tweet,
        'comments': comments,
        'form': form,
    }
    return render(request, 'tweet_detail.html', context)

@login_required
def like_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    like, created = Like.objects.get_or_create(tweet=tweet, user=request.user) # get_or_create tries to find a Like object for this tweet + user.
    if not created:  # If it exists → created = False . If it doesn’t exist → creates a new Like → created = True
        like.delete()  # toggle unlike
    # Redirect back to the page the user came from
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def repost_tweet(request, pk):
    original = get_object_or_404(Tweet, pk=pk)  # Fetches the tweet that the user wants to repost.
    Tweet.objects.create(user=request.user, text=original.text, photo=original.photo, reposted_from=original)
# Creates a new Tweet with:
# user=request.user → the current logged-in user becomes the author of the new tweet.
# text=original.text → copies the original text.
# photo=original.photo → copies the original photo.
# reposted_from=original → links the new tweet to the original one (so you know it’s a repost).
    # Redirect back to the page the user came from
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()   # Save the user
            # Save avatar to Profile
            if 'avatar' in request.FILES:
                profile = user.profile  # assumes Profile exists
                profile.avatar = request.FILES['avatar']
                profile.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'registration/register.html', {'form': form})