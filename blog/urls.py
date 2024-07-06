from django.urls import path
# from . import views
from .views import faqs,contact,PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,likeView

urlpatterns = [
    # path('', views.home, name = "blog-home"),
    path('', PostListView.as_view(), name = "blog-home"),
    path('post/<int:pk>/', PostDetailView.as_view(), name = "post-detail"),
    path('user/<str:username>/', UserPostListView.as_view(), name = "user-posts"),
    path('post/new/', PostCreateView.as_view(), name = "post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = "post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = "post-delete"),
    path('faqs/', faqs, name = "blog-faqs"),
    path('contact/', contact, name = "blog-contact"),
    path('like/<int:pk>', likeView, name = "like-post"),
]
