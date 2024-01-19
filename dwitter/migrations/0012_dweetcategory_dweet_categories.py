# Generated by Django 4.2.4 on 2024-01-19 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0011_remove_comment_name_comment_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DweetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='dweet',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='dweetcatagories', to='dwitter.dweetcategory'),
        ),
    ]