from django.urls import path
from account.views.user_view import UserView
from account.views.obtain_token_view import ObtainTokenView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('user/', UserView.as_view()),
    path('user/<int:id>/', UserView.as_view()),
    path('login/', ObtainTokenView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('verify-token/', TokenVerifyView.as_view()),
]
