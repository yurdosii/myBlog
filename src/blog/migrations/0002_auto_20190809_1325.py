# Generated by Django 2.2.4 on 2019-08-09 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'managed': True, 'ordering': ['-publish_date', '-updated', '-timestamp'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
    ]
