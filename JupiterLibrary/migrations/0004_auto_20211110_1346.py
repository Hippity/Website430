# Generated by Django 3.2.7 on 2021-11-10 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JupiterLibrary', '0003_alter_book_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='numberAvailable',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='numberBorrowed',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
