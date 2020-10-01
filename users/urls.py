from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIProfile, UserViewSet, send_code, send_token

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='User')


urlpatterns = [
    path('auth/email/', send_code),
    path('auth/token/', send_token),
    path('users/me/', APIProfile.as_view()),
    path('', include(router_v1.urls)),

]
