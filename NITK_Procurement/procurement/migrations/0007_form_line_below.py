# Generated by Django 4.2.3 on 2023-10-30 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0006_section_line_below'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='line_below',
            field=models.BooleanField(default=False),
        ),
    ]
