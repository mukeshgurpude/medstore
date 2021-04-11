# Generated by Django 3.1 on 2020-09-08 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.PositiveBigIntegerField(null=True, verbose_name='Mobile Number'),
        ),
    ]