# Generated by Django 4.1.1 on 2022-10-09 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otpcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otpcode',
            options={'ordering': ('-created_at',)},
        ),
    ]
