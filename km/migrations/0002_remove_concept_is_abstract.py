# Generated by Django 3.1.4 on 2020-12-25 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concept',
            name='is_abstract',
        ),
    ]