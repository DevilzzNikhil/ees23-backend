# Generated by Django 3.2.7 on 2021-12-02 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udyam_API', '0005_remove_team_number_of_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='submission',
            field=models.CharField(default='Not Submitted', max_length=40),
        ),
    ]
