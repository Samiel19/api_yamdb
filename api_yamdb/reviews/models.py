from django.db import models

from users.models import User

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


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=32, unique=True, db_index=True)

    class Meta:
        verbose_name = 'genre'

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=32, unique=True, db_index=True)

    class Meta:
        verbose_name = 'category'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField()
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='genre',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='category',
    )
    description = models.TextField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'title'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    score = models.IntegerField(choices=RATING_CHOICES, default=1)

    def __str__(self):
        return f'{self.title.name, self.author.username, self.score}'

    class Meta:
        default_related_name = "reviews"
        verbose_name = "review"
        verbose_name_plural = "reviews"
        ordering = ['-pub_date']
        constraints = (
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='author_title'),)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = "comments"
        default_related_name = "comments"
