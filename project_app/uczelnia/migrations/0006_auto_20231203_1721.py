# Generated by Django 3.2.18 on 2023-12-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uczelnia', '0005_alter_news_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='semester',
            field=models.CharField(default='2023/2024', max_length=100),
        ),
        migrations.AlterField(
            model_name='subject',
            name='semester',
            field=models.CharField(default='2023/2024', max_length=100),
        ),
    ]
