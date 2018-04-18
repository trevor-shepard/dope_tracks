# Generated by Django 2.0.3 on 2018-04-13 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('external_url', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to='images/album')),
                ('mbid', models.CharField(max_length=128)),
                ('spotify_id', models.CharField(blank=True, max_length=128, null=True)),
                ('spotify_url', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('popularity', models.IntegerField(blank=True, null=True)),
                ('followers', models.IntegerField(blank=True, null=True)),
                ('mbid', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/artist')),
                ('spotify_id', models.CharField(blank=True, max_length=128, null=True)),
                ('spotify_url', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('summary', models.CharField(blank=True, max_length=800, null=True)),
                ('image', models.ImageField(upload_to='images/group')),
                ('public', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', related_query_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('wiki_url', models.CharField(blank=True, max_length=300, null=True)),
                ('image', models.ImageField(upload_to='images/tag')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('external_url', models.CharField(blank=True, max_length=500, null=True)),
                ('popularity', models.IntegerField(blank=True, null=True)),
                ('url', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='images/track')),
                ('mbid', models.CharField(max_length=128)),
                ('spotify_id', models.CharField(blank=True, max_length=128, null=True)),
                ('spotify_url', models.CharField(blank=True, max_length=128, null=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track', related_query_name='track', to='info.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='UserTrackHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_track_history', related_query_name='user_track_history', to='info.Track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_history', related_query_name='track_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='tags',
            field=models.ManyToManyField(related_name='group_tags', to='info.Tag'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artist',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='artist_tags', related_query_name='artist_tags', to='info.Tag'),
        ),
    ]
