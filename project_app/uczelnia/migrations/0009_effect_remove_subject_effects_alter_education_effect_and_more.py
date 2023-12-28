# Generated by Django 5.0 on 2023-12-09 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uczelnia', '0008_rename_text_education_effect'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='subject',
            name='effects',
        ),
        migrations.AlterField(
            model_name='education',
            name='effect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uczelnia.effect'),
        ),
        migrations.AddField(
            model_name='subject',
            name='effects',
            field=models.ManyToManyField(related_name='subjects', to='uczelnia.effect'),
        ),
    ]
