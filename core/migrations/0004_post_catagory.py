# Generated by Django 3.0.3 on 2020-03-21 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200321_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='catagory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='core.catagories'),
        ),
    ]
