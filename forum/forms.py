# From Django
from django.forms import ModelForm

# From models
from models import Topic, Post

# Create the form class.
class AddTopicForm(ModelForm):
    class Meta:
        model = Topic # Mentions the model
        # Specify the fields to exclude (Those are auto-populated, and to be hidden)
        exclude=['forum','created','updated','creator','views','closed','post_count','last_post']

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        # Specify the fiels to include, all others are excluded
        fields=['title','description']