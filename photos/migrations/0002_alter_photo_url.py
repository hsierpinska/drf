# Generated by Django 3.2.16 on 2022-10-27 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.CharField(max_length=255),
        ),
    ]