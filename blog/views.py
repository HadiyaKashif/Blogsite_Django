import urllib.request, urllib.parse
import json

from django.shortcuts import render, get_object_or_404,redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import ContactForm, NewCommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

# posts = [
#         {
#         'title' : '1st blog',
#         'name' : 'Hadiya Kashif',
#         'date_posted' : '21/02/2024',
#         'content' : 'This is the first dummy post'
#         },
#         {
#         'title' : '2nd blog',
#         'name' : 'H K',
#         'date_posted' : '22/02/2024',
#         'content' : 'This is the second dummy post'
#         }
#         ]

# def home(request):
#     context = {'posts' : Post.objects.all()}
#     return render(request,'home.html',context)

#there are multiple types of built in views like list view, detail view that displays details, update view etc
class PostListView(ListView):
    model = Post
    template_name = 'home.html' #specified this because by default it will search for template on path <app>/<model>_<viewname>.html
    context_object_name = 'posts' #specified this because by default django expects 'object' in template while we have written 'posts' (like post.author or post.title)
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):  #function to display only first sentence on homepage
        queryset = super().get_queryset() #getting all posts from DB
        for post in queryset:
            first_full_stop_index = post.content.find('.')
            if first_full_stop_index != -1:  #if a full stop is found
                post.content = post.content[:first_full_stop_index + 1]  #content to be displayed from start to the first occurence of full stop. +1 to include the '.' too
                post.truncated = True
            else:
                post.truncated = False
        return queryset

class UserPostListView(ListView):
    model = Post
    template_name = 'user_posts.html' #specified this because by default it will search for template on path <app>/<model>_<viewname>.html
    context_object_name = 'posts' #specified this because by default django expects 'object' in template while we have written 'posts' (like post.author or post.title)
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        queryset = Post.objects.filter(author=user).order_by('-date_posted')
        for post in queryset:
            first_full_stop_index = post.content.find('.')
            if first_full_stop_index != -1:  #if a full stop is found
                post.content = post.content[:first_full_stop_index + 1]  #content to be displayed from start to the first occurence of full stop. +1 to include the '.' too
                post.truncated = True
            else:
                post.truncated = False
        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'Post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(post=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = Comment(message=request.POST.get('message'),
                                  author=self.request.user,
                                  post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView): #loginrequiredmixins should be written prior so that it is asked before performing further action
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'
    # success_url = '/'  rredirects to homepage

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #UserPassesTestMixins is used to check whether the one asking to update is the author of post or not
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'
    # success_url = '/' 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def likeView(request,pk):
    post = get_object_or_404(Post,id = pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))

def faqs(request):
    return render(request,'faqs.html',{'title' : 'FAQs'})
# def contact(request):
#     return render(request,'contact.html',{'title' : 'Contact'})
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Begin reCAPTCHA validation  :this part is from https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            #also some urllib functions are different from the site I copied (It said urllib2) because apparently there are some modificatins now. Mostly follwed stackoverflow here
            #https://stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode
            data = urllib.parse.urlencode(values).encode("utf-8") #here used encode after seeing from stackoverflow, because the func was returning string but POST data which is sent to urlopen must be in bytes
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            result = json.load(response)
            # End reCAPTCHA validation 

            if result['success']:
                form.save()
                username = form.cleaned_data.get('name')
                messages.success(request,f'Message by {username} sent successfully!')
                
            else:
                messages.error(request, 'reCAPTCHA failed. Please try again.')
            
            # form.save()
            return redirect('/contact/')
    else:
        form = ContactForm()

    return render(request,'contact.html',{'form' : form})