from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# import datetime
# Create your models here.
User = get_user_model


class Genres(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    title = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(unique=True)
    # genres = models.ForeignKey(
    #     Genres,
    #     # on_delete=models.CASCADE
    # )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    RATING_CHOICES = (
        (10, '10'),
        (9, '9'),
        (8, '8'),
        (7, '7'),
        (6, '6'),
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    )
    # Произведение
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)
    # Отзыв
    text = models.TextField()
    # Юзер , нужно изменить!
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     default=1,
    #     on_delete=models.CASCADE
    # )
    # Дата
    # pub_date = models.DateTimeField(
    #     auto_now_add=True,
    #     verbose_name='Publication Date'
    # )
    # publish = models.DateTimeField(default=datetime.timezone.now)   # время когда опубликовано
    created = models.DateTimeField(auto_now_add=True)   # время создания
    updated = models.DateTimeField(auto_now=True)   # время редактирования
    # Коммент
    comment = models.TextField(max_length=1024)
    # Оценка от 1 до 5
    value = models.IntegerField(choices=RATING_CHOICES, default=1)

    # def __str__(self):
    #     return '{0}/{1} - {2}'.format(self.book.title, self.user.username, self.value)

    class Meta:
        verbose_name = "Titles Review"
        verbose_name_plural = "Titles Reviews"
        ordering = ['-pub_date']


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "comments"
        default_related_name = "comments"