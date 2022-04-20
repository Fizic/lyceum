# Generated by Django 3.2.12 on 2022-04-20 11:06

import catalog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_item_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default='роскошно', validators=[catalog.validators.text_validator], verbose_name='описание'),
        ),
    ]
