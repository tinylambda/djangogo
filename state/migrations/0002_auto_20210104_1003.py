# Generated by Django 3.1.4 on 2021-01-04 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='is_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='state.state', verbose_name='Parent State'),
        ),
    ]
