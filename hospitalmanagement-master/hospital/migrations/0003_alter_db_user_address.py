# Generated by Django 4.1.7 on 2023-03-02 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_db_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_user',
            name='address',
            field=models.CharField(max_length=40),
        ),
    ]