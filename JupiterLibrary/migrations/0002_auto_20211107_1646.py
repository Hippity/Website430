# Generated by Django 3.2.7 on 2021-11-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JupiterLibrary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publicationData',
            new_name='publicationDate',
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
