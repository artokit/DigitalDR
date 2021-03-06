# Generated by Django 3.1.7 on 2022-02-19 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0011_auto_20220218_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='digitalDR.customuser')),
                ('n', models.TextField()),
            ],
            bases=('digitalDR.customuser',),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='Y05gRVxVut3a0NN7pkMCYnbADRMDG9ILCjFRaAAC', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='teacher_code',
            field=models.CharField(default='xmgORGdApM8aqqbk', max_length=16, unique=True, verbose_name='Код'),
        ),
    ]
