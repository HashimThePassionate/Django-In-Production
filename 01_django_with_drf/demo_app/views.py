from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from demo_app import  custom_versions

class DemoView(APIView):
    versioning_class = custom_versions.DemoViewVersion

    def get(self, request, *args, **kwargs):
        version = request.version
        return Response(data={'message':f'You have hit {version} version of the Demo-api'})

class AnotherView(APIView):
    versioning_class = custom_versions.AnotherViewVersion
    def get(self, request, *args, **kwargs):
        version = request.version
        if version == 'v1':
            return Response({'message': f'V1 Logic goes here'})
        elif version == 'v2':
            return Response({'message': f'V2 Logic goes here'})
     


@api_view(['GET'])
def hello_world(request, *atrgs, **kwargs):
    return Response(data={'message': 'Hello, World!'})


@api_view(['GET'])
def demo_version(request, *args, **kwargs):
    version = request.version
    return Response(data={'message':f'You have hit {version} version of the Demo-api'})