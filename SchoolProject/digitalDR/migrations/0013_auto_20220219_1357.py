# Generated by Django 3.1.7 on 2022-02-19 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitalDR', '0012_auto_20220219_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='teacher_code',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='n',
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_teacher',
            field=models.BooleanField(default=True, verbose_name='Учитель'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default='MLbXa2NFjqfgnf8j', max_length=16, unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cookie',
            field=models.CharField(default='LDzIIiOaArE0m0tRDHGNRMkLq8riDK5sNCvVuF1E', max_length=40, unique=True),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='digitalDR.customuser')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='Учитель')),
            ],
            bases=('digitalDR.customuser',),
        ),
    ]
