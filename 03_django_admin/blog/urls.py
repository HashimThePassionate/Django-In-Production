from django.urls import path
from . import views

urlpatterns = [
    path('api/blogs/', views.BlogGetCreateView.as_view(), name='blog-get-create'),
    path('api/blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('api/blogs/create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('api/blogs/list/', views.BlogListView.as_view(), name='blog-list'),
    path('api/blogs/<int:pk>/retrieve/', views.BlogRetrieveView.as_view(), name='blog-retrieve'),
    path('api/blogs/<int:pk>/delete/', views.BlogDestroyView.as_view(), name='blog-delete'),
    path('api/blogs/<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('api/blogs/list-create/', views.BlogListCreateView.as_view(), name='blog-list-create'),
    path('api/blogs/<int:pk>/retrieve-update/', views.BlogRetrieveUpdateView.as_view(), name='blog-retrieve-update'),
    path('api/blogs/custom/', views.BlogGetUpdateView.as_view(), name='blog-custom'),
    path('api/blogs/ordered/', views.BlogGetUpdateFilterView.as_view(), name='blog-ordered'),
    path('api/blogs/search/', views.BlogSearchView.as_view(), name='blog-search'),

]