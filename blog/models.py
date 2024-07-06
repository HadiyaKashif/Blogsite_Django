from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Post(models.Model):
    title = models.CharField(max_length=100)
    # content = RichTextField(blank = True, null = True)
    content = CKEditor5Field(blank = True, null = True, config_name='extends')
    # content = models.TextField(blank = True, null = True)
    date_posted = models.DateTimeField(default = timezone.now)
    #auto_now updates the date each time a change is made in field
    #auto_now_add adds the date of only when the object was created can't be modified afterwards
    #default = timezone.now allows us to change date
    author = models.ForeignKey(User, on_delete = models.CASCADE) #.CASCADE tells that if author is deleted then post is deleted too
    likes = models.ManyToManyField(User,related_name="blog_posts")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk}) # used to redirect to detailed view of post, can be redirected to home page by ussing success url in views
    
class Contact(models.Model): 
    name = models.CharField(max_length=70)
    email = models.EmailField()
    subject = models.CharField(max_length=100, default='')
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.subject

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name = "comments",on_delete = models.CASCADE) #.CASCADE tells that if author is deleted then post is deleted too
    author = models.ForeignKey(User, on_delete = models.CASCADE) #.CASCADE tells that if author is deleted then post is deleted too
    message = models.TextField()
    date_posted = models.DateTimeField(default = timezone.localtime)
    
    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post.title)