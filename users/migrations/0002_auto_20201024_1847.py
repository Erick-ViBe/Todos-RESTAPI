# Generated by Django 3.1.2 on 2020-10-24 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todouser',
            name='color',
            field=models.CharField(choices=[('pink', 'Pink'), ('blue', 'Blue'), ('green', 'Green'), ('aquamarine', 'Aquamarine'), ('coral', 'Coral'), ('brown', 'Brown')], default='aquamarine', max_length=10),
        ),
    ]
