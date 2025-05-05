from django.urls import path
from . import views

urlpatterns = [
    path('api/blogs/', views.BlogGetCreateView.as_view(), name='blog-get-create'),
    path('api/blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
]