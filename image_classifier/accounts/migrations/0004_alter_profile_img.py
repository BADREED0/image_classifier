# Generated by Django 5.0.3 on 2024-04-18 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, height_field=models.PositiveIntegerField(default=300), upload_to='profile-image/', width_field=models.PositiveIntegerField(default=300)),
        ),
    ]
