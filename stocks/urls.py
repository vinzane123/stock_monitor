from django.contrib import admin
from django.urls import path, include 
from rest_framework.schemas import get_schema_view
from .views import LoginView,LogoutView,StockSearch,WatchList,WatchListbyUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/login',LoginView.as_view()),
    path('api/v1/auth/logout',LogoutView.as_view()),
    path('api/v1/stock_search',StockSearch.as_view()),
    path('api/v1/watch_list',WatchList.as_view()),
    path('api/v1/watch_list/<int:id>',WatchList.as_view()),
    path('api/v1/watch_list_user',WatchListbyUser.as_view()),
]


