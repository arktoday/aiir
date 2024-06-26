# Generated by Django 5.0.3 on 2024-05-19 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0006_accesshistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField()),
                ('result', models.JSONField(default={})),
            ],
            options={
                'db_table': 'operation',
            },
        ),
    ]
