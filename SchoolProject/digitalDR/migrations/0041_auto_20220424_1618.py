# Generated by Django 3.1.7 on 2022-04-24 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0040_auto_20220417_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='balance_last_info',
        ),
        migrations.RemoveField(
            model_name='userinformation',
            name='balance_last_time',
        ),
    ]
