# Generated by Django 3.1.5 on 2021-11-25 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
