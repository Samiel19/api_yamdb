import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Title, Genre, Category, Review, Comment,
)  
from users.models import User 


TABLES = {
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    User: 'users.csv',
}


class ImportCommand(BaseCommand):

    def main(self, *args, **kwargs):
        for model, csv_file in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r', encoding='utf-8'
            ) as import_csv_file:
                reader = csv.DictReader(import_csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('The data was uploaded successfully'))
