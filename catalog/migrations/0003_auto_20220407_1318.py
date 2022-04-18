# Generated by Django 3.2.12 on 2022-04-07 08:18

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_item_text'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('catalog_item_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_items', to='catalog.category', verbose_name='категория'),
        ),
    ]
