from rest_framework import serializers
from django.shortcuts import get_object_or_404

from api.validators import validate_username
from api_yamdb.settings import BANNED_SYMBOLS
from reviews.models import (RATING_CHOICES, Category, Comment, Genre, Review,
                            Title)
from users.models import User


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )
    score = serializers.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')

        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            author = self.context['request'].user
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(
                author=author, title=title
            ).exists():
                raise serializers.ValidationError(['Нельзя'])
        return data


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        validators = (validate_username,)
        fields = (
            'username', 'email', 'bio', 'role', 'first_name', 'last_name',
        )


class UserAuthSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=BANNED_SYMBOLS,
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        validators = (validate_username,)
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
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'genre',
            'category',
            'year',
            'rating',
            'description',
        )
        read_only_fields = (
            'id',
            'name',
            'genre',
            'category',
            'year',
            'rating',
            'description',
        )


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
        model = Title
        fields = (
            'id',
            'name',
            'genre',
            'category',
            'year',
            'description',
        )
