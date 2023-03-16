from reviews.models import Review, Comment, RATING_CHOICES
from rest_framework import serializers

from users.models import User


class ReviewSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    value = serializers.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        fieds = '__all__'
        model = Review
        read_only_fields = ('titles', )


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', )       
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role', 'first_name', 'last_name',
        )

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username
    
    
class UserAuthSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserRegisterSerializer(serializers.ModelSerializer):
    

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        if User.objects.filter(email=data['username']).exists():
            raise serializers.ValidationError('Пользователь с таким username уже существует')
        if data['username'] == 'me':
            raise serializers.ValidationError('me вам ещё понадобится!')
        return data

    class Meta:
        model = User
        fields = ('username', 'email')
