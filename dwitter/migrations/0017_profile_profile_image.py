# Generated by Django 4.2.4 on 2024-01-20 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0016_alter_dweet_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
