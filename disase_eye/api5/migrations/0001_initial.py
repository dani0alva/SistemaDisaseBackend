# Generated by Django 4.1.5 on 2023-01-25 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('empresa_id', models.AutoField(primary_key=True, serialize=False)),
                ('empresa_ruc', models.CharField(max_length=15, unique=True, verbose_name='R.U.C.')),
                ('empresa_rs', models.CharField(max_length=100, unique=True, verbose_name='Razon Social')),
                ('empresa_ubi', models.CharField(max_length=200, verbose_name='Ubicacion')),
                ('empresa_tel', models.CharField(max_length=15, verbose_name='Telefono')),
                ('empresa_mail', models.EmailField(max_length=50, unique=True, verbose_name='Email')),
                ('empresa_web', models.CharField(max_length=75, null=True, verbose_name='Pagina Web')),
                ('empresa_fech_cre', models.DateTimeField(null=True, verbose_name='Fecha de creacion')),
                ('empresa_fech_mod', models.DateTimeField(null=True, verbose_name='Fecha de modificacion')),
                ('empresa_est', models.BooleanField(default=True, verbose_name='Estado de la empresa')),
            ],
            options={
                'db_table': 'tbl_empresa',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('usu_id', models.AutoField(primary_key=True, serialize=False)),
                ('usu_doc', models.CharField(choices=[('DNI', 'DNI'), ('PASAPORTE', 'Pasaporte'), ('CARNET', 'Carnet de Extranjeria'), ('LIBRETA', 'Libreta Electoral')], max_length=25, verbose_name='Tipo Documento')),
                ('usu_nroDoc', models.CharField(max_length=15, unique=True, verbose_name='Nro documento')),
                ('usu_tel', models.CharField(max_length=15, verbose_name='Telefono')),
                ('usu_sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=50, verbose_name='Sexo')),
                ('cargo', models.CharField(max_length=50, verbose_name='Cargo')),
                ('usu_fech_cre', models.DateTimeField(null=True, verbose_name='Fecha de creacion')),
                ('usu_fech_mod', models.DateTimeField(null=True, verbose_name='Fecha de modificacion')),
                ('usu_est', models.BooleanField(default=True, verbose_name='Estado del usuario')),
                ('empresa_id', models.ForeignKey(db_column='empresa_id', on_delete=django.db.models.deletion.CASCADE, related_name='usuario_empresa', to='api5.empresa')),
                ('usuario_id', models.OneToOneField(db_column='usuario_id', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'db_table': 'tbl_usuario',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('paciente_id', models.AutoField(primary_key=True, serialize=False)),
                ('paciente_ciudad', models.CharField(max_length=50, verbose_name='ciudad')),
                ('paciente_pais', models.CharField(max_length=50, verbose_name='pais')),
                ('paciente_doc', models.CharField(choices=[('DNI', 'DNI'), ('PASAPORTE', 'Pasaporte'), ('CARNET', 'Carnet de Extranjeria'), ('LIBRETA', 'Libreta Electoral')], max_length=25, verbose_name='Tipo Documento')),
                ('paciente_nroDoc', models.CharField(max_length=15, unique=True, verbose_name='Nro documento')),
                ('paciente_sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=50, verbose_name='Sexo')),
                ('paciente_tel', models.CharField(max_length=15, verbose_name='Telefono')),
                ('paciente_dir', models.CharField(max_length=250, verbose_name='Direccion')),
                ('paciente_fechanac', models.DateField(null=True)),
                ('paciente_fech_cre', models.DateTimeField(null=True, verbose_name='Fecha de creacion')),
                ('paciente_fech_mod', models.DateTimeField(null=True, verbose_name='Fecha de modificacion')),
                ('paciente_est', models.BooleanField(default=True, verbose_name='Estado del paciente')),
                ('empresa_id', models.ForeignKey(db_column='empresa_id', on_delete=django.db.models.deletion.CASCADE, related_name='paciente_empresa', to='api5.empresa')),
                ('usuario_id', models.OneToOneField(db_column='usuario_id', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'db_table': 'tbl_paciente',
            },
        ),
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('diag_id', models.AutoField(primary_key=True, serialize=False)),
                ('diag_disease', models.CharField(choices=[('RETINO', 'Retinopatia'), ('GLAUCOMA', 'Glaucoma'), ('CATARATAS', 'cataratas')], max_length=25, verbose_name='Tipo de Enfermedad')),
                ('diag_img_eye_right', models.ImageField(blank='', default='', upload_to='retinopatia/eye_right')),
                ('diag_img_eye_left', models.ImageField(blank='', default='', upload_to='retinopatia/eye_left')),
                ('diag_nivel_disease_right', models.IntegerField(blank=True, null=True)),
                ('diag_nivel_disease_left', models.IntegerField(blank=True, null=True)),
                ('diag_nivel_disease_change_right', models.IntegerField(blank=True, null=True)),
                ('diag_nivel_disease_change_left', models.IntegerField(blank=True, null=True)),
                ('diag_fech_cre', models.DateTimeField(null=True, verbose_name='Fecha de creacion')),
                ('diag_fech_mod', models.DateTimeField(null=True, verbose_name='Fecha de modificacion')),
                ('diag_est', models.BooleanField(default=True, verbose_name='Estado del Diagnostico')),
                ('paciente_id', models.ForeignKey(db_column='paciente_id', on_delete=django.db.models.deletion.RESTRICT, related_name='paciente_diagnostico', to='api5.paciente')),
            ],
            options={
                'db_table': 'tbl_diagnostico',
            },
        ),
    ]
