import re  # re = Regular Expressions module (used to find patterns in text)

from django import template  # Used to create custom template filters in Django
from django.urls import reverse  # Used to generate URL from a URL name

# Create a template library object
# This is required to register custom filters
register = template.Library()


# Register this function as a custom template filter
@register.filter
def render_hashtags(value):
    """
    This function finds all #hashtags in the text
    and converts them into clickable links.
    """

    # This function will be called every time
    # a hashtag match is found in the text
    def replace_tag(match):

        # match.group(1) gives the word after '#'
        # Example: If text is "#Python"
        # group(1) will give "Python"
        tag_name = match.group(1).lower()  # convert tag to lowercase for consistency

        # reverse() generates URL using the URL name
        # 'tagged_tweets' must match the name in your urls.py
        # args=[tag_name] passes the tag name as parameter
        # tag/python/

        url = reverse('tagged_tweets', args=[tag_name])


        # Return HTML anchor tag
        # This replaces the plain hashtag with a clickable link
        # Example output:
        # <a href="/tags/python/" class="text-blue-400 hover:underline">#python</a>
        return f'<a href="{url}" class="text-blue-400 hover:underline">#{tag_name}</a>'

    # Regex pattern:
    # '#'  → match the hashtag symbol
    # (\w+) → match one or more word characters (letters, numbers, underscore)
    # The word inside brackets () is captured as group(1)
    pattern = r'#(\w+)'

    # re.sub() searches the text (value)
    # For every hashtag found, it calls replace_tag()
    # and replaces the hashtag with clickable HTML
    return re.sub(pattern, replace_tag, value)
