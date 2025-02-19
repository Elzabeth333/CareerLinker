# Generated by Django 5.1.1 on 2024-09-29 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0011_jobs_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='education',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='key_skills',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='preferred_candidate_profile',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='role',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
