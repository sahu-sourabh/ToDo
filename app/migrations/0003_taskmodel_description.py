# Generated by Django 3.2.5 on 2021-09-07 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210902_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]