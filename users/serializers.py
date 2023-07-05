from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = User
        fields = ['email', 'name', 'username',  'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Both Passwords must be same.')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'username', 'is_active']
        

class PasswordChangeSerializer(serializers.Serializer):

    password = serializers.CharField(max_length= 255,style={'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(max_length= 255,style={'input_type':'password'}, write_only= True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Both Passwords must be same.')
        user.set_password(password)
        user.save()
        return attrs


class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['username'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active

        return token