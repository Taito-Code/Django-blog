# Generated by Django 2.2.5 on 2021-02-01 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210130_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='pv',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
