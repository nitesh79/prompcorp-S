# Generated by Django 5.1.1 on 2024-10-01 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcapp', '0017_alter_materialinvoice_individual_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='myfile',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
