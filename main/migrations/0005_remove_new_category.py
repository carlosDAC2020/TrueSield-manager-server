# Generated by Django 5.0.2 on 2024-04-24 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_new_rss_url_new_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='category',
        ),
    ]
