# Generated by Django 4.2.5 on 2023-10-06 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixtures',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]