# Generated by Django 5.1 on 2024-08-27 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
