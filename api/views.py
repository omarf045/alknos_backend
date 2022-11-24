# Create your views here.
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

import os
from django.conf import settings 

from .inorganic_reaction_utils import react

from rest_framework.parsers import MultiPartParser

from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
# Class based view to Get User Details using Token Authentication

import threading

# custom thread
class ProductsThread(threading.Thread):
    # constructor
    def __init__(self, compounds):
        # execute the base constructor
        threading.Thread.__init__(self)
        # set a default value
        self.products = None
        self.compounds = compounds
 
    # function executed in a new thread
    def run(self):
        self.products = react(self.compounds)


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Class based view to register user
class RegisterUserAPI(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class InorganicReactionAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        compounds = request.data['compounds']

        thread = ProductsThread(compounds)
        # start the thread
        thread.start()
        # wait for the thread to finish
        thread.join()
        # report all values returned from a thread
        products = thread.products

        return Response(data=products)
