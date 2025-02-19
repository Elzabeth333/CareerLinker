# Generated by Django 5.1.1 on 2024-09-29 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0008_alter_company_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='company_reviews',
        ),
        migrations.RemoveField(
            model_name='jobs',
            name='department',
        ),
        migrations.RemoveField(
            model_name='jobs',
            name='role_category',
        ),
        migrations.AlterField(
            model_name='jobs',
            name='education',
            field=models.CharField(choices=[("Bachelor's Degree", "Bachelor's Degree"), ("Master's Degree", "Master's Degree"), ('B.Tech/B.E. in Computers', 'B.Tech/B.E. in Computers'), ('M.Tech/M.E. in Computers', 'M.Tech/M.E. in Computers'), ('Bachelors in Data Science', 'Bachelors in Data Science'), ('Masters in Data Science', 'Masters in Data Science'), ('Bachelors in Engineering', 'Bachelors in Engineering'), ('Masters in Engineering', 'Masters in Engineering'), ('Primary Education', 'Primary Education'), ('Lower Secondary Education', 'Lower Secondary Education'), ('Upper Secondary Education', 'Upper Secondary Education'), ('Associate Degree', 'Associate Degree'), ('Doctoral Degree', 'Doctoral Degree'), ('Certificate Programs', 'Certificate Programs'), ('Diploma Programs', 'Diploma Programs'), ('MD (Doctor of Medicine)', 'MD (Doctor of Medicine)'), ('MBBS (Bachelor of Medicine, Bachelor of Surgery)', 'MBBS (Bachelor of Medicine, Bachelor of Surgery)'), ('DO (Doctor of Osteopathy)', 'DO (Doctor of Osteopathy)'), ('JD (Juris Doctor)', 'JD (Juris Doctor)'), ('LLB (Bachelor of Laws)', 'LLB (Bachelor of Laws)'), ('LLM (Master of Laws)', 'LLM (Master of Laws)'), ('DVM (Doctor of Veterinary Medicine)', 'DVM (Doctor of Veterinary Medicine)'), ('DDS (Doctor of Dental Surgery)', 'DDS (Doctor of Dental Surgery)'), ('Online Courses', 'Online Courses'), ('Adult Education', 'Adult Education'), ('Technical and Vocational Education and Training (TVET)', 'Technical and Vocational Education and Training (TVET)'), ('Military Education', 'Military Education'), ('Other', 'Other')], default='B.Tech/B.E. in Computers', max_length=255),
        ),
    ]
