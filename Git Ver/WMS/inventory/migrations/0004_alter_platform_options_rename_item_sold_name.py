# Generated by Django 4.2.4 on 2023-09-15 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_platform_sold'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='platform',
            options={'verbose_name_plural': 'Platforms'},
        ),
        migrations.RenameField(
            model_name='sold',
            old_name='item',
            new_name='name',
        ),
    ]
