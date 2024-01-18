# Generated by Django 4.2.4 on 2024-01-18 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0009_alter_dweet_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('dweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dwitter.dweet')),
            ],
        ),
    ]