# Generated by Django 5.0.7 on 2024-08-06 16:07

import clientspace.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientspace', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=clientspace.models.user_files_path),
        ),
    ]
