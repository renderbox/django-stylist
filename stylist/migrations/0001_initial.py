# Generated by Django 3.1.2 on 2020-10-09 00:25

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', unique_with=('site__id',), verbose_name='Slug')),
                ('attrs', models.JSONField(blank=True, default=dict)),
                ('enabled', models.BooleanField(verbose_name='Enabled')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_style', to='sites.site')),
            ],
            options={
                'verbose_name': 'Site Style',
                'verbose_name_plural': 'Site Styles',
            },
        ),
    ]
