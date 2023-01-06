# dwitter/urls.py
from django.urls import include,path
from .views import dashboard, profile_list, profile,register
#  app name deleted try to  solve problem 
# app_name = "dwitter"
urlpatterns = [
path("dashboard", dashboard, name="dashboard"),
path("profile_list/", profile_list, name="profile_list"),
path("profile/<int:pk>", profile, name="profile"),
path("accounts/", include("django.contrib.auth.urls")),
path('oauth/', include('social_django.urls', namespace='social')), # <-- here
path("register/", register, name="register"),
]