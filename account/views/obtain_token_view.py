from rest_framework_simplejwt.views import TokenObtainPairView
from account.serializers.obtain_token_serializer import ObtainTokenSerializer


class ObtainTokenView(TokenObtainPairView):
    serializer_class = ObtainTokenSerializer
