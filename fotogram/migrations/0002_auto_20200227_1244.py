# Generated by Django 2.2.9 on 2020-02-27 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fotogram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='photos'),
        ),
    ]