# Generated by Django 3.0.3 on 2020-06-07 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200531_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcode',
            name='verify_code',
            field=models.CharField(default='mtKkdOuRRz', max_length=10, unique=True),
        ),
    ]
