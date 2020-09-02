from .views import send_code, send_token, UserViewSet, APIProfile

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='User')


urlpatterns = [
    path('auth/email/', send_code),
    path('auth/token/', send_token),
    path('users/me/', APIProfile.as_view()),
    path('', include(router_v1.urls)),

]
