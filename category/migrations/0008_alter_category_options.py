# Generated by Django 4.0.5 on 2022-06-21 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'managed': True, 'ordering': ('name',)},
        ),
    ]
