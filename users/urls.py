from django.urls import path
from .views import RegisterView, LoginView, GetUserDataFromToken,CreateNewAccessToken
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     ToekenVerifyView
# )

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', GetUserDataFromToken.as_view()),
    path('create-access', CreateNewAccessToken.as_view())
    # path('jwt/create/', TokenObtainPairView.as_view(), name="jwt_create"),
    # path('jwt/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    # path('jwt/verify/', ToekenVerifyView.as_view(), name="token_verify"),
]
