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
import requests
import urllib.request

from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token


response_data = None
# Create your views here.
class CompoundQueryAPI(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        query = request.data['query']
        query = query.upper()

        def get_compounds_by_cid(cids):
            response_data = []
            cids = list(filter(lambda x: x != '', cids))
            request_cids = ','.join(map(str, cids))

            compounds_url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{request_cids}/property/MolecularFormula,MolecularWeight,IUPACName/JSON'
            compounds_response = requests.get(compounds_url)
            compounds_data = json.loads(compounds_response.text)
            compounds = compounds_data['PropertyTable']['Properties']

            synonyms_url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{request_cids}/synonyms/JSON'
            synonyms_response = requests.get(synonyms_url)
            synonyms_data = json.loads(synonyms_response.text)
            synonyms = synonyms_data['InformationList']['Information']

            for i, compound in enumerate(compounds):
                common_name = synonyms[i]["Synonym"][0]
                response_data.append({"cid": compound['CID'], "common_name":common_name ,"iupac_name" : compound['IUPACName'], "molecular_formula": compound['MolecularFormula'], "molecular_weight": compound['MolecularWeight'], "2d_thumbnail": f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={compound['CID']}&t=s" })

            return response_data

        def get_compounds():
            global response_data
            url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(query)}/cids/TXT?name_type=word'

            response = requests.get(url)

            if response.status_code == 200:
                cids = response.text.split('\n')[:15]
                response_data = get_compounds_by_cid(cids)
            elif response.status_code == 404:
                url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{urllib.parse.quote(query)}/cids/TXT'
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    print(f"Error {response.status_code} - {response.reason}: {e}")
                    return Response(status=response.status_code)
                cids = response.text.split('\n')[:15]
                response_data = get_compounds_by_cid(cids)
            else:
                print(f"Error {response.status_code} - {response.reason}: {e}")
                return Response(status=response.status_code)
                                
        thread = threading.Thread(target=get_compounds)
        thread.start()
        thread.join()
        return Response(response_data)
    
