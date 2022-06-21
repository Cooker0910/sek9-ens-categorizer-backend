# Generated by Django 4.0.5 on 2022-06-20 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial'),
        ('ethereum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethereum',
            options={'managed': True, 'ordering': ('category', 'name', 'domain')},
        ),
        migrations.AlterUniqueTogether(
            name='ethereum',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='ethereum',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='domain_ethereums', to='domain.domain'),
        ),
        migrations.AlterUniqueTogether(
            name='ethereum',
            unique_together={('name', 'domain')},
        ),
    ]
