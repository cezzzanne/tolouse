# Generated by Django 2.0.5 on 2019-01-01 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('unique_id', models.CharField(max_length=200)),
                ('playlist_id', models.TextField(null=True)),
                ('user_id', models.CharField(max_length=200, null=True)),
                ('access_token', models.TextField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('token_info', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member', to='src.Party'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL),
        ),
    ]
