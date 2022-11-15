from turtle import pos
from webbrowser import get
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from User.models import CustomUser
from django.contrib.auth import get_user
from .models import Post
from .serializers import PostSerializer
# Create your views here.


@login_required(login_url='/api/user/authFailedError')
@api_view(['POST'])
def createPost(request):
    data = request.data
    try:
        description = data['description']
        img = data['img']
        currUser = get_user(request)
        post = Post.objects.create(
            postedBy = currUser,
            description = description,
            img = img
        )
        postSerializer = PostSerializer(post, many = False)
        return Response({'post':postSerializer.data},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errorMessage":"Error occured in creating post","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getPost(self,id):
    try:
        post = Post.objects.get(
            postId = id
        )
        postSerializer = PostSerializer(post,many=False)
        return Response({'post':postSerializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':"No post found by id : "+str(id)},status=status.HTTP_404_NOT_FOUND)


@login_required(login_url='/api/user/authFailedError')
@api_view(['GET'])
def getAllPosts(request):
    try:
        currUser = get_user(request)
        posts = Post.objects.filter(
            postedBy = currUser
        )
        postSerializer = PostSerializer(posts,many=True)
        return Response({'posts':postSerializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_404_NOT_FOUND)


@login_required(login_url='/api/user/authFailedError')
@api_view(['PATCH'])
def updatePost(request,id):
    data = request.data
    try:
        currUser = get_user(request)
        description = data['description']
        img = data['img']
        try:
            post = Post.objects.get(
                postId = id,
                postedBy = currUser
            )
            post.description = description
            post.img = img
            post.save()
        except Exception as e:
            return Response({'errorMessage':"You are not authorized to update this post"},status=status.HTTP_401_UNAUTHORIZED)
        
        postSerializer = PostSerializer(post,many=False)
        return Response({"message":"Update successful.",'post':postSerializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@login_required(login_url='/api/user/authFailedError')
@api_view(['DELETE'])
def deletePost(request,id):
    try:
        currUser = get_user(request)
        try:
            post = Post.objects.get(
                postId = id,
                postedBy = currUser
            )
            post.delete()
        except Exception as e:
            return Response({'errorMessage':"You are not authorized to delete this post."},status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message":"Delete successful."},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required(login_url='/api/user/authFailedError')
@api_view(['PATCH'])
def likeUnlikePost(request,id):
    try:
        currUser = get_user(request)
        post = Post.objects.get(
            postId = id
        )
        likedByList = list(post.likedBy.all())
        if currUser in likedByList:
            post.likedBy.remove(currUser)
            post.save()
            return Response({'message':"UnLike operation successful.!!!"})
        else:
            post.likedBy.add(currUser)
            post.save()
            return Response({'message':"Like operation successful.!!!"})
    except Exception as e:
        return Response({'errorMessage':str(e)},status=status.HTTP_404_NOT_FOUND)


