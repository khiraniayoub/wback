from django.contrib import admin
from django.urls import path, include 
from users.views import UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
