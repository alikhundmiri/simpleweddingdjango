# Generated by Django 3.0.3 on 2020-06-07 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200607_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcode',
            name='verify_code',
            field=models.CharField(default='UfpAVzzdOO', max_length=10, unique=True),
        ),
    ]