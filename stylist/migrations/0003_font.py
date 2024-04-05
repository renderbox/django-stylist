# Generated by Django 3.1.2 on 2024-04-05 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stylist', '0002_auto_20210114_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=50, verbose_name='Font Family')),
                ('href', models.URLField(verbose_name='URL')),
                ('provider', models.CharField(help_text='Ex: google', max_length=50, verbose_name='Provider')),
                ('meta', models.JSONField(blank=True, default=dict, help_text="any extra meta data we'd like to store as json")),
                ('weights', models.JSONField(blank=True, default=list)),
                ('preferred', models.BooleanField(default=False, verbose_name='Preferred')),
            ],
            options={
                'verbose_name': 'Font',
                'verbose_name_plural': 'Fonts',
                'ordering': ['-preferred', 'family'],
            },
        ),
    ]