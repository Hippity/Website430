# Generated by Django 3.2.7 on 2021-11-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JupiterLibrary', '0011_remove_userinfo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='fName',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='lName',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
