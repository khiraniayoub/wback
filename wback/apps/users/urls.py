from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegistrationView, UserViewSet, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    #path('profile/', ProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
