# Generated by Django 4.2.5 on 2023-10-03 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_lead_date_added_lead_description_lead_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='Category',
            new_name='category',
        ),
    ]
