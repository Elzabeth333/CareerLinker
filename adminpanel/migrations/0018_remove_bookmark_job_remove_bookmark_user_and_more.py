# Generated by Django 5.1.1 on 2024-09-30 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0017_applicationnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='job',
        ),
        migrations.RemoveField(
            model_name='bookmark',
            name='user',
        ),
        migrations.AddField(
            model_name='job',
            name='selected_candidates',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Applicant',
        ),
        migrations.DeleteModel(
            name='Bookmark',
        ),
    ]
