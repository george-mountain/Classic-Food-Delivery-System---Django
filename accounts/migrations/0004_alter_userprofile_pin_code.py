# Generated by Django 4.1.1 on 2022-10-05 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_address_line_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pin_code',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
