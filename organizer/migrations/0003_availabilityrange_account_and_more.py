# Generated by Django 4.0.2 on 2022-03-25 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizer', '0002_watchparty_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabilityrange',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availabilityrange',
            name='watchparty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organizer.watchparty'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AddedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watchparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.watchparty')),
            ],
        ),
    ]
