# Generated by Django 5.1.2 on 2024-11-05 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_main.project'),
        ),
    ]
