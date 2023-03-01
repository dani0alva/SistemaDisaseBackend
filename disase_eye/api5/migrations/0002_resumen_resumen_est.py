# Generated by Django 4.1.5 on 2023-01-26 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api5', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resumen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa_id', models.IntegerField(blank=True, null=True)),
                ('año', models.IntegerField(blank=True, null=True)),
                ('mes', models.CharField(max_length=20, unique=True, verbose_name='MES_DESC')),
            ],
            options={
                'db_table': 'tbl_resumen',
            },
        ),
        migrations.CreateModel(
            name='Resumen_est',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa_id', models.IntegerField(blank=True, null=True)),
                ('año', models.IntegerField(blank=True, null=True)),
                ('mes', models.CharField(max_length=20, unique=True, verbose_name='MES_DESC')),
                ('cantidad', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_resumen_est',
            },
        ),
    ]
