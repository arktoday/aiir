# Generated by Django 5.0.3 on 2024-04-29 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_alter_source_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
