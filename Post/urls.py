from django.urls import path

from . import views

urlpatterns = [
    path('create',views.createPost,name='createPost'),
    path('getPost/<str:id>',views.getPost,name='getPost'),
    path('getAllPosts',views.getAllPosts,name='getAllPosts'),
    path('update/<str:id>',views.updatePost,name='updatePost'),
    path('delete/<str:id>',views.deletePost,name='deletePost'),
    path('likeUnlikePost/<str:id>',views.likeUnlikePost,name='likeUnlikePost'),
]