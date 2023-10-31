# Generated by Django 4.2.3 on 2023-10-30 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0002_question_align_type_question_bold'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='bold',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='align_type',
            field=models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='bold',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_type',
            field=models.CharField(choices=[('left', 'Left'), ('center', 'Center'), ('flex', 'Flex')], max_length=50),
        ),
    ]