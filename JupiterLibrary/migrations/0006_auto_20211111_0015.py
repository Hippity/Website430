# Generated by Django 3.2.7 on 2021-11-10 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JupiterLibrary', '0005_rename_publicationdate_book_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authorFirstName',
            field=models.CharField(max_length=50, verbose_name='Author First Name'),
        ),
        migrations.AlterField(
            model_name='book',
            name='authorLastName',
            field=models.CharField(max_length=50, verbose_name='Author Last Name'),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, height_field=306, upload_to='images/', width_field=475),
        ),
        migrations.AlterField(
            model_name='book',
            name='numberAvailable',
            field=models.IntegerField(verbose_name='Number Available'),
        ),
        migrations.AlterField(
            model_name='book',
            name='numberBorrowed',
            field=models.IntegerField(verbose_name='Number Borrowed'),
        ),
    ]