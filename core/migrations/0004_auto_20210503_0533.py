# Generated by Django 3.2 on 2021-05-03 05:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210502_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='created_by',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='employee',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='last_updated_by',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='employee',
            name='last_updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
