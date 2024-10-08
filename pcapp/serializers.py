# myapp/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims (like email and username)
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user information to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.name,
            'email': self.user.email,
            # Add any other fields you'd like to return
        }

        return data
