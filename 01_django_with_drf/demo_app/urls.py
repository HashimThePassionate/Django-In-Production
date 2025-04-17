from django.urls import path
from demo_app import views


urlpatterns = [
    path('hello-world/', views.hello_world),
    path('demo-version/', views.demo_version),
    path('custom-version/',views.DemoView.as_view()),
    path('another-custom-version/',views.AnotherView.as_view()),
]
