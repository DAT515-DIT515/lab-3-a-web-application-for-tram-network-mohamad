# Generated by Django 5.0 on 2023-12-11 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep', models.CharField(max_length=200)),
                ('dest', models.CharField(max_length=200)),
            ],
        ),
    ]
