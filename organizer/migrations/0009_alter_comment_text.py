# Generated by Django 4.0.2 on 2022-04-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0008_favoritemovie_delete_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=10000),
        ),
    ]