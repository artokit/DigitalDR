# Generated by Django 3.1.7 on 2022-04-16 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0037_auto_20220410_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='profile_image',
        ),
    ]