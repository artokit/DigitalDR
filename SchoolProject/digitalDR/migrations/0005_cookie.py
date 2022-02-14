# Generated by Django 3.1.7 on 2022-02-05 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0004_auto_20220205_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie', models.CharField(default='tIOPSympP0sWwvdtsr2Tv52NBwPKUbbS9OBzh08b', max_length=40, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='digitalDR.customuser')),
            ],
        ),
    ]
