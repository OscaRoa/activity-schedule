# Generated by Django 2.2.24 on 2021-08-21 17:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('schedule', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('c', 'canceled'), ('a', 'active'), ('d', 'done')], default='a', max_length=35)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_id', to='properties.Property')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answers', django.contrib.postgres.fields.jsonb.JSONField()),
                ('activity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='activities.Activity')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
