# Generated by Django 4.1.5 on 2023-01-30 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api5', '0007_alter_diagnostico_diag_rnrodoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumen_est',
            name='disase',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Nombre de Enfermedad'),
        ),
        migrations.AlterField(
            model_name='resumen_est',
            name='mes',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='MES_DESC'),
        ),
    ]
