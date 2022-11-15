from turtle import pos
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser,Profile
from .serializers import CustomUserSerializer,ProfileSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import jwt
from django.contrib.auth import get_user
from Post.models import Post
from Post.serializers import PostSerializer
# Create your views here.


# secret key for jwt token
SECRET_KEY_FOR_TOKEN = "harsh@6519@7295@KEY"

## this will be called when user is not authenticated.!!!
@api_view(['GET'])
def authFailedError(request):
    return Response({"errorMessage":"Authentication Failed.!!"},status=status.HTTP_401_UNAUTHORIZED)


# user's controller
@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        
        password = data['password']
        name = data['name']
        email = data['email']
        try:
            user = CustomUser.objects.get(email = email)
            return Response({"erorMessage":"Email already exists, Try different one."},status=status.HTTP_226_IM_USED)
        except:
            try:
                user = CustomUser.objects.create(email = email)
                user.set_password(password)
                user.save()
                profile = Profile.objects.create(user = user,name = name)
                userSerializer = CustomUserSerializer(user,many=False)
                profileSerializer = ProfileSerializer(profile,many=False)
                return Response({
                    "email":user.email,
                    "profile":profileSerializer.data
                },status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "errorMessage":"Error occured during creation of user",
                    "error":str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    except:
        return Response({"erorMessage":"Please provide all fields email, name and password."},status=status.HTTP_400_BAD_REQUEST)
                
    
@api_view(['POST'])
def loginUser(request):
    data = request.data
    try:
        email = data['email']
        password = data['password']
        user = authenticate(request, username = email, password = password)
        if(user is None):
            return Response({"errorMessage":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                login(request,user)
                CurrUser = CustomUser.objects.get(email = email)
                profile = Profile.objects.get(user = CurrUser)    
                token = jwt.encode(payload={
                    "name":profile.name,
                    "email":email,
                    "password":password,
                },key=SECRET_KEY_FOR_TOKEN,algorithm='HS256')
                return Response({
                    "name":profile.name,
                    "email":str(user),
                    "token":token},status=status.HTTP_200_OK)
            except:
                return Response({"errorMessage":"Error occured during authentication."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({"erorMessage":"Please provide both fields email  and password."},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logoutUser(request):
    try:
        logout(request)
        return Response({"Message":"Logout successful"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errorMessage":"Error occured during loging out","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)     



@login_required(login_url='/api/user/authFailedError')
@api_view(['PATCH'])
def updatePassword(request):
    data = request.data
    try:
        oldPassword = data['oldpassword']
        newpassword = data['newpassword']
        email = data['email']
        try:
            user = authenticate(request, username = email, password = oldPassword)
            if user is None:
                return Response({"errorMessage":"Invalid credentials, Try again.!!"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                CurrUser = CustomUser.objects.get(email = user)
                CurrUser.set_password(newpassword)
                CurrUser.save()
                return Response({"message":"Password updated.!!!"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errorMessage":str(e)})
    except Exception as e:
        return Response({"errorMessage":"Please provide all fields email, oldpassword and newpassword"},status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/api/user/authFailedError')
@api_view(['DELETE'])
def deleteMyAccount(request):
    # when we delete user, then we need to remove following stuffs:
        # 1> deleteing posts posted by user
        # 2> removing likes done on any posts
        # 3> remove email from followers list of users, whom this user earlier have followed
        # 4> remove email from followings list of user, who earlier followed this user 
    try:
        currUserEmail = get_user(request)
        currUser = CustomUser.objects.get(email = currUserEmail)
        currUserProfile = Profile.objects.get(user = currUser)

        ## 1> deleting posts posted by currUser
        #myPostsIds = list(currUser.post_set.all())
        #for item in myPostsIds:
        #    post = Post.objects.get(postId = item.postId)
        #    post.delete()

        ## 2> removing likes done on any post
        #posts = Post.objects.all()
        #for item in posts:
        #    likedBy = list(item.likedBy.all())
        #    if currUser in likedBy:
        #        item.likedBy.remove(currUser)
        #        item.save()

        ## 3> removing email from followers list of other user which are earlier followed by curruser
        


        return Response({'ed':'ed'})
    except Exception as e:
        return Response({"errorMessage":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getProfile(request,email):
    try:
        user = CustomUser.objects.get(email = email)
        profile = Profile.objects.get(user = user)
        profileSerializer = ProfileSerializer(profile,many = False)
        return Response({
            "email":user.email,
            "profile":profileSerializer.data
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errorMessage":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getMyProfile(request):
    try:
        currUser = get_user(request)
        profile = Profile.objects.get(
            user = currUser   
        )
        profileSerializer = ProfileSerializer(profile,many=False)
        return Response({"profile":profileSerializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errorMessage":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@login_required(login_url='/api/user/authFailedError')
@api_view(['PATCH'])
def updateProfile(request):
    data = request.data
    try:
        currUser = get_user(request)
        name = data['name']
        about = data['about']
        profilePicture = data['profilePicture']
        coverPicture = data['coverPicture']
        profile = Profile.objects.get(
            user = currUser
        )
        profile.name = name
        profile.about = about
        profile.profilePicture = profilePicture
        profile.coverPicture = coverPicture
        profile.save()
        return Response({'message':'Profile updated.!!!'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# follow related controllers

@login_required(login_url='/api/user/authFailedError')
@api_view(['POST'])
def followUser(request,email):
    try:
        currEmail = get_user(request)
        currUser = CustomUser.objects.get(
            email = currEmail
        )
        currUserProfile = Profile.objects.get(
            profileId = currUser.profile.profileId
        )
        user = CustomUser.objects.get(
            email = email
        )
        userProfile = Profile.objects.get(
            profileId = user.profile.profileId
        )
        if currUser.email == user.email:
            return Response({'errorMessage':'You can not follow/unfollow yourself.!!'},status=status.HTTP_400_BAD_REQUEST)
        else:
            userFollowers = list(userProfile.followers.all())
            if currUser in userFollowers:
                return Response({'errorMessage':"You already follow this user"},status=status.HTTP_400_BAD_REQUEST)
            
            userProfile.followers.add(currUser.email)
            userProfile.save()
            currUserProfile.followings.add(user.email)
            currUserProfile.save()
        return Response({'message':'Follow operation successful.!!'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='/api/user/authFailedError')
@api_view(['POST'])
def unFollowUser(request,email):
    try:
        currEmail = get_user(request)
        currUser = CustomUser.objects.get(
            email = currEmail
        )
        currUserProfile = Profile.objects.get(
            profileId = currUser.profile.profileId
        )
        user = CustomUser.objects.get(
            email = email
        )
        userProfile = Profile.objects.get(
            profileId = user.profile.profileId
        )
        if currUser.email == user.email:
            return Response({'errorMessage':'You can not follow/unfollow yourself.!!'},status=status.HTTP_400_BAD_REQUEST)
        else:
            userFollowers = list(userProfile.followers.all())
            if currUser not in userFollowers:
                return Response({'errorMessage':"You can not unfollow this user, because you are not following it"},status=status.HTTP_400_BAD_REQUEST)
            
            userProfile.followers.remove(currUser.email)
            userProfile.save()
            currUserProfile.followings.remove(user.email)
            currUserProfile.save()
        return Response({'message':'unFollow operation successful.!!'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def myFollowers(request):
    try:
        currUser = get_user(request)
        profile = Profile.objects.get(
            user = currUser
        )
        profileSerialzer = ProfileSerializer(profile,many=False)
        return Response({'followers':profileSerialzer.data['followers']},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def myFollowings(request):
    try:
        currUser = get_user(request)
        profile = Profile.objects.get(
            user = currUser
        )
        profileSerialzer = ProfileSerializer(profile,many=False)
        return Response({'followings':profileSerialzer.data['followings']},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getFollowers(request,email):
    try:
        user = CustomUser.objects.get(
            email = email
        )
        profile = Profile.objects.get(
            user = user
        )
        profileSerialzer = ProfileSerializer(profile,many=False)
        return Response({'followers':profileSerialzer.data['followers']},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getFollowings(request,email):
    try:
        user = CustomUser.objects.get(
            email = email
        )
        profile = Profile.objects.get(
            user = user
        )
        profileSerialzer = ProfileSerializer(profile,many=False)
        return Response({'followings':profileSerialzer.data['followings']},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getMyLikedPosts(request):
    try:
        currUserEmail = get_user(request)
        currUser = CustomUser.objects.get(
            email = currUserEmail
        )
        likedPosts = currUser.likedBy.all()
        posts = []
        for item in likedPosts:
            post = Post.objects.get(
                postId = item.postId
            )
            postSerializer = PostSerializer(post,many=False)
            posts.append(postSerializer.data)
        return Response({'myLikedPosts':posts},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getFeed(request):
    try:
        currUserEmail = get_user(request)
        currUser = CustomUser.objects.get(email = currUserEmail)
        currUserProfile = Profile.objects.get(user = currUser)
        currUserProfileSerializer = ProfileSerializer(currUserProfile,many=False)
        # feed will be posts that are posted by user itself + posts of user that her is following

        # my posts
        myPostsIds = list(currUser.post_set.all())
        myPosts = []
        for item in myPostsIds:
            post = Post.objects.get(postId = item.postId)
            postSerializer = PostSerializer(post,many=False)
            myPosts.append(postSerializer.data)
        
        # posts of user that i follow
        postsByFollowings = []
        followings = currUserProfileSerializer.data['followings']
        for item in followings:
            user = CustomUser.objects.get(email = item)
            postIds = user.post_set.all()
            for post in postIds:
                temp = Post.objects.get(postId = post.postId)
                tempSerializer = PostSerializer(temp,many=False)
                postsByFollowings.append(tempSerializer.data)
        
        feed = myPosts + postsByFollowings
        return Response({'Feed':feed},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    