# Generated by Django 5.0.8 on 2024-08-07 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utensil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.CharField(max_length=255)),
                ('status', models.BooleanField()),
                ('utensil', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='detection.utensil')),
            ],
        ),
    ]
