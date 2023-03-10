# Generated by Django 4.0.2 on 2022-04-08 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizer', '0003_availabilityrange_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieSearcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=100)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watchparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.watchparty')),
            ],
        ),
    ]
