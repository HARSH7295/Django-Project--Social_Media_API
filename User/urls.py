from django.urls import path
from . import views

urlpatterns = [
    path('registerUser',views.registerUser,name = 'RegisterUser'),
    path('loginUser',views.loginUser,name = 'loginUser'),
    path('logoutUser',views.logoutUser,name='logoutUser'),

    path('authFailedError',views.authFailedError,name='authFailedError'),

    path('updatePassword',views.updatePassword,name = 'updatePassword'),
    path('deleteMyAccount',views.deleteMyAccount,name = 'deleteMyAccount'),
    
    path('getProfile/<str:email>',views.getProfile,name = 'getProfile'),
    path('getMyProfile',views.getMyProfile,name='getMyProfile'),
    path('updateProfile',views.updateProfile,name = 'updateProfile'),

    path('followUser/<str:email>',views.followUser,name = 'followUser'),
    path('unFollowUser/<str:email>',views.unFollowUser,name = 'unFollowUser'),

    path('myFollowers',views.myFollowers,name='myFollowers'),
    path('myFollowings',views.myFollowings,name='myFollowings'),

    
    path('<str:email>/getFollowers',views.getFollowers,name='getFollowers'),
    path('<str:email>/getFollowings',views.getFollowings,name='getFollowings'),

    path('getMyLikedPosts',views.getMyLikedPosts,name='getMyLikedPosts'),

    path('getFeed',views.getFeed,name='getFeed'),
]