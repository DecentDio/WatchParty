# Generated by Django 4.0.2 on 2022-04-23 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0011_rename_selected_time_finalizedwatchparty_selected_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finalizedwatchparty',
            old_name='selected_date',
            new_name='selected_time',
        ),
    ]
