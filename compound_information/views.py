# Create your views here.
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions

import os
from django.conf import settings 

import pubchempy as pcp

import threading

from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token

# Create your views here.
class CompoundQueryAPI(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        query = request.data['query']
        print(query)
        response_data = []

        def get_compounds():
            results = pcp.get_compounds(query, 'name',listkey_count=15)

            if not results:
                try:
                    results = pcp.get_compounds(query, 'formula',listkey_count=15)
                except pcp.BadRequestError:
                    results = []

            for result in results:
                cid = result._record["id"]["id"]["cid"]
                response_data.append({"cid": cid,"iupac_name" : result.iupac_name, "molecular_formula": result.molecular_formula, "molecular_weight": result.molecular_weight, "2d_thumbnail": "https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid="+str(cid)+"&t=s" })

                            
        thread = threading.Thread(target=get_compounds)
        thread.start()
        thread.join()
        return Response(response_data)
