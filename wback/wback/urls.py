from django.contrib import admin
from django.urls import path, include 
from usuarios.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),

    path('', include('usuarios.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
