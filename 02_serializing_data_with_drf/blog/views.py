from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
        b_obj = serializers.BlogSerializer(
            blog_instance, data=input_data, partial=True)
        if b_obj.is_valid():
            b_obj.save()
            return Response(b_obj.data, status=status.HTTP_200_OK)
        return Response(data=b_obj.errors, status=status.HTTP_400_BAD_REQUEST)


# Generics Views

class BlogCreateView(generics.CreateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


class BlogListView(generics.ListAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


class BlogRetrieveView(generics.RetrieveAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


class BlogDestroyView(generics.DestroyAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


class BlogUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


class BlogListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


class BlogRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()


#  Customization with query_set method

class BlogGetUpdateView(generics.ListCreateAPIView):
    serializer_class = serializers.BlogSerializer

    def get_queryset(self):
        blog = models.Blog.objects.filter(id__gt=3)
        return blog

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Filters

class BlogGetUpdateFilterView(generics.ListAPIView):
    serializer_class = serializers.BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']  
    ordering = 'title' 

    def get_queryset(self):
        return models.Blog.objects.all()
    

class BlogSearchView(generics.ListAPIView):
    serializer_class = serializers.BlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content'] 

    def get_queryset(self):
        return models.Blog.objects.all()