# Generated by Django 3.0.6 on 2020-05-28 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20200525_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('SME_USER', 'SME_USER'), ('INVESTOR_USER', 'INVESTOR_USER'), ('BACKOFFICE_USER', 'BACKOFFICE_USER')], default='BACKOFFICE_USER', max_length=225),
        ),
    ]
