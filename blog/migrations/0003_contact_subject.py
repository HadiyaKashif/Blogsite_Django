# Generated by Django 5.0.2 on 2024-03-13 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.TextField(default='No subject', max_length=100),
        ),
    ]
