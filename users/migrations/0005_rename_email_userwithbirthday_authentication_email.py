# Generated by Django 3.2.12 on 2022-04-20 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userwithbirthday_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userwithbirthday',
            old_name='email',
            new_name='authentication_email',
        ),
    ]
