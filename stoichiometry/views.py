# Create your views here.
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions

import threading
import requests
import urllib.request

from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token

from chemlib import Reaction, Compound

# Create your views here.
class BalanceReactionAPI(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response_data = None
        reaction = Reaction.by_formula(request.data['reaction'])
        reaction.balance()
        response_data = [str(reaction)]
            
        return Response({"reaction": response_data})

class CalculateStoichiometryAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        reaction = Reaction.by_formula(request.data['reaction'])
        stoichiometry_unit = request.data['unit']
        stoichiometry_value = request.data['value']
        compound_position = request.data['position']

        if (stoichiometry_unit=='moles'):
            stoichiometry_reaction = reaction.get_amounts(compound_position, moles=stoichiometry_value)
        elif (stoichiometry_unit=='grams'):
            



        return Response(stoichiometry_reaction)