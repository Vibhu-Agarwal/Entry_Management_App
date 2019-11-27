# Generated by Django 2.2.7 on 2019-11-27 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20191127_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managementtokenauth',
            name='host_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='managementtokenauth',
            name='token_given',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]