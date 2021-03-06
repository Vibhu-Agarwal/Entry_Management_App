# Generated by Django 2.2.7 on 2019-11-23 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191121_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Holmes Home', max_length=1024, verbose_name='Full name')),
                ('address1', models.CharField(default='221B Baker Street', max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(default=None, max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.CharField(default='NW1 6XE', max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(default='London', max_length=1024, verbose_name='City')),
                ('country', models.CharField(default='England', max_length=1024, verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Office Branch',
                'verbose_name_plural': 'Office Branches',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='office_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='users.OfficeBranch'),
        ),
    ]
