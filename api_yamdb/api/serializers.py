from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from reviews.models import (
    Review, Comment, RATING_CHOICES,
    Title, Category, Genre,
)


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

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя me запрещено'
            )     
        return data
    
    def validate_role(self, role):
        try:
            if self.instance.role != 'admin':
                return self.instance.role
            return role
        except AttributeError:
             return role


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
        if data['username'] == 'me':
            raise serializers.ValidationError('me вам ещё понадобится!')
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Такой username уже есть'
            )
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Такой email уже есть'
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    value = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title
