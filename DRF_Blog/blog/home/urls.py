from django.urls import path

from home.views import BlogView,publicView

urlpatterns =[
    path('blog/',BlogView.as_view()),
    path('public/',publicView.as_view())
]