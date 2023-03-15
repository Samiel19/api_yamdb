from reviews.models import Review, Comment, RATING_CHOICES
from rest_framework import serializers


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
