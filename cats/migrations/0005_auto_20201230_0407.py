# Generated by Django 3.1.4 on 2020-12-30 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0004_auto_20201229_1826'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='cat',
            constraint=models.CheckConstraint(check=models.Q(age__gt=0), name='cat_age_gt_zero'),
        ),
    ]