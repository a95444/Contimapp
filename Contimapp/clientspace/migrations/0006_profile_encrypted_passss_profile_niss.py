# Generated by Django 5.0.7 on 2024-08-08 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientspace', '0005_alter_file_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='encrypted_passSS',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='niss',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
