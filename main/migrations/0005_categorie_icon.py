# Generated by Django 3.0.3 on 2020-05-10 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200505_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='icon',
            field=models.CharField(default='name', max_length=80),
        ),
    ]
