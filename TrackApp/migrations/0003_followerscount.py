# Generated by Django 4.1.7 on 2023-04-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrackApp', '0002_alter_profile_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
