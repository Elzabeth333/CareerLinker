# Generated by Django 5.1.1 on 2024-09-27 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]
