# Generated by Django 4.2.16 on 2024-09-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst_app', '0003_alter_csvmodel_current_employee_estimate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvmodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
