# Generated by Django 5.2.3 on 2025-07-31 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trackinghistory',
            old_name='expense',
            new_name='expense_type',
        ),
    ]
