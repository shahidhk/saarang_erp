from django.forms import ModelForm
from models import Topic, Post

# Create the form class.
class AddTopicForm(ModelForm):
    class Meta:
        model = Topic
        #fields=['forum','title','updated','creator','closed','usertags','iswork','post_count','last_post']
        exclude=['forum','created','updated','creator','views','closed','post_count','last_post']

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields=['title','description']