from django.urls import path,include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.vendorDashboard, name='vendor'), #making use of the account views to reroute traffic from vendor url.
    path('profile/', views.vprofile, name='vprofile'),
    
   
] 
