from multiprocessing import AuthenticationError
from User.models import CustomUser
from django.shortcuts import redirect
class CustomMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        ## code to be executed before requrest sent to view
        ## just got the request here,,,

        if(not request.user.is_authenticated()):
            raise AuthenticationError("Authentication Invalid.!!")

        # above this line all things to request can be done        
        response = self.get_response(request)
        # below this line all things to response can be done

        ## code to be execured after request sent to view
        ## request is already sent to view and just got response
        
        
        return response

    

# add below line in middleware of settings for activating this middleware

    #'Custom_Middleware.Middleware.CustomMiddleware',