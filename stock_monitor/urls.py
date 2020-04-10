from django.contrib import admin
from django.urls import path, include 
from rest_framework.schemas import get_schema_view
from stocks.views import LoginView,LogoutView,StockSearch,WatchList,WatchListbyUser,index,loginpage

urlpatterns = [
    path('', include('stocks.urls')),
    path('login/',loginpage,name='page_login'),
    path('',index,name='index'),
]


