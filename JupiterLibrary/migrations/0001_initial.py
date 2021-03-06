# Generated by Django 3.2.7 on 2021-11-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('authorFirstName', models.CharField(max_length=50)),
                ('authorLastName', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=30)),
                ('publicationData', models.DateField()),
                ('image', models.ImageField(upload_to='')),
                ('genre', models.TextField()),
                ('synopsis', models.TextField()),
            ],
        ),
    ]
