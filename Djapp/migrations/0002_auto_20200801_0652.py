# Generated by Django 3.0.7 on 2020-08-01 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Djapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='data_of_birth',
            new_name='date_of_birth',
        ),
    ]
