# Generated by Django 3.1.7 on 2021-03-23 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit_recipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
