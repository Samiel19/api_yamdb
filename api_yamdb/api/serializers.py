from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role'
        )


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        if data['username'] == 'me':
            raise serializers.ValidationError('me вам ещё понадобится!')
        return data

    class Meta:
        model = User
        fields = ('username', 'email')