from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include 
from rest_framework.schemas import get_schema_view
from stocks.views import LoginView,LogoutView,StockSearch,WatchList,WatchListbyUser,index

urlpatterns = [
    path('', include('stocks.urls')),
    # path('login/',loginpage,name='page_login'),
    path('',index,name='index'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


