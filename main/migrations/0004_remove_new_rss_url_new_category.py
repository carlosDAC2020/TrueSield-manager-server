# Generated by Django 5.0.2 on 2024-04-24 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_new_rss_url_alter_new_body_alter_new_summary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='rss_url',
        ),
        migrations.AddField(
            model_name='new',
            name='category',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
