# Generated by Django 3.2.18 on 2023-12-02 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uczelnia', '0003_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='semester',
            field=models.IntegerField(default=1),
        ),
    ]
