from rest_framework.viewsets import ModelViewSet
from .serializers import ReviewSerializers, CommentSerializers
from reviews.models import Review, Comment, Titles
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class TitleViewSet(ModelViewSet):
    pass


class CategoryViewSet(ModelViewSet):
    pass


class GenreViewSet(ModelViewSet):
    pass


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = (permissions.IsAuthenticated, )

    @property
    def titles_get(self):
        return get_object_or_404(Titles, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, titles=self.titles_get)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение запрещено')
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Удаление запрещено')
        return super().perform_destroy(serializer)

    def get_queryset(self):
        return self.titles_get.reviews.all()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = (permissions.IsAuthenticated, )

    @property
    def review_get(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reviews=self.review_get)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение запрещено')
        return super().perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Удаление запрещено')
        return super().perform_destroy(serializer)

    def get_queryset(self):
        return self.review_get.comment.all()
