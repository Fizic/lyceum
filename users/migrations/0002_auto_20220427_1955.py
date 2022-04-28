# Generated by Django 3.2.12 on 2022-04-27 14:55

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extendeduser',
            options={'ordering': ['email'], 'verbose_name': 'Расширенный пользователь', 'verbose_name_plural': 'Расширенные пользователи'},
        ),
        migrations.AlterModelManagers(
            name='extendeduser',
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
