from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ObtainTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(ObtainTokenSerializer, self).validate(attrs)
        user_data = {
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'username': self.user.username,
        }
        data.update({'user': user_data})
        return data