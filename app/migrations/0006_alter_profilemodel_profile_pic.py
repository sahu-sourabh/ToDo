# Generated by Django 3.2.5 on 2021-09-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profilemodel_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='profile_pic',
            field=models.ImageField(default='Buddha.jpg', upload_to='profile_pics'),
        ),
    ]