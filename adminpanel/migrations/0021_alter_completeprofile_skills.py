# Generated by Django 5.1.1 on 2024-10-01 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0020_alter_applicationnotification_applicant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completeprofile',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='users', to='adminpanel.skill'),
        ),
    ]
