from django.urls import path
from accounts import views as Accountviews
from . import views

urlpatterns =[
     path('', Accountviews.custDashboard, name='customer'),
     path('profile/',views.cprofile, name='cprofile'),
]