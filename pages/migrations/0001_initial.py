# Generated by Django 3.0 on 2020-05-03 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('experiment_id', models.CharField(default='chdl-[1234]', max_length=12, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('methods_intro', models.TextField(default='Enter a long description of the experiment')),
                ('methods', models.TextField()),
                ('query', models.TextField()),
                ('conclusion_1', models.TextField(verbose_name='what we learned')),
                ('conclusion_2', models.TextField(verbose_name='further investigation')),
            ],
            options={
                'db_table': 'labReports',
            },
        ),
    ]
