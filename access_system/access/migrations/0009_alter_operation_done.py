# Generated by Django 5.0.3 on 2024-05-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0008_alter_operation_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]