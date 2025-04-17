from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_world(request, *atrgs, **kwargs):
    return Response(data={'message': 'Hello, World!'})


@api_view(['GET'])
def demo_version(request, *args, **kwargs):
    version = request.version
    return Response(data={'message':f'You have hit {version} version of the Demo-api'})