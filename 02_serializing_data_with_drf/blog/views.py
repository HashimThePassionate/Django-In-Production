from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers

class BlogGetCreateView(views.APIView):
    def get(self, request):
        blogs_obj_list = models.Blog.objects.all()
        blogs = serializers.BlogSerializer(blogs_obj_list, many=True)
        return Response(blogs.data)

    def post(self, request):
        input_data = request.data
        b_obj = serializers.BlogSerializer(data=input_data)
        if b_obj.is_valid():
            b_obj.save()
            return Response(b_obj.data, status=status.HTTP_201_CREATED)
        return Response(data=b_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogDetailView(views.APIView):
    def get(self, request, pk):
        try:
            blog_instance = models.Blog.objects.get(pk=pk)
            blog = serializers.BlogSerializer(blog_instance)
            return Response(blog.data)
        except models.Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            blog_instance = models.Blog.objects.get(pk=pk)
        except models.Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        input_data = request.data
        b_obj = serializers.BlogSerializer(blog_instance, data=input_data)
        if b_obj.is_valid():
            b_obj.save()
            return Response(b_obj.data, status=status.HTTP_200_OK)
        return Response(data=b_obj.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            blog_instance = models.Blog.objects.get(pk=pk)
        except models.Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        input_data = request.data
        b_obj = serializers.BlogSerializer(blog_instance, data=input_data, partial=True)
        if b_obj.is_valid():
            b_obj.save()
            return Response(b_obj.data, status=status.HTTP_200_OK)
        return Response(data=b_obj.errors, status=status.HTTP_400_BAD_REQUEST)