import datetime
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.forms import ModelForm 
import time
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

import datetime
import os
import unicodedata


def logo_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        ''' 
        company_instance = Empresa.objects.get(pk=instance.empresa_id)
        if company_instance.empresa_log:
            logo = company_instance.empresa_log
            if logo.file:
                print("llego aqui",logo)
                print("la ruta es :",logo.file)
                
                if os.path.isfile(logo.path):
                    
                    
                    logo.file.close()
                    os.remove(logo.path)
                    
        '''
        return os.path.join('disases/logo', filename)

class PathAndRename():
    """
    fields to use for naming, order is important
    """

    def __init__(self, path,posicion):
        self.path = path
        self.posicion = posicion

    def wrapper(self, instance, filename):
        ext = filename.split('.')[-1]
        nom_archivo = filename.split('.')[0]
        mes = time.strftime('%y%m')
        hora_actual = datetime.datetime.now()
        dia=''

        if(len(str(hora_actual.day))==2):
            dia=str(hora_actual.day)

        else:
            dia='0'+str(hora_actual.day)

        #instance_type = type(instance).__name__
        filename = '{}.{}'.format(uuid4().hex, ext)
        #name = str(instance.pk)+'_'+str(instance.paciente_id.paciente_nroDoc)+'_'+dia+'_'+str(hora_actual.hour)+''+str(hora_actual.minute)+''+str(hora_actual.second)+'_'+nom_archivo
        
       
        #filename = '{}.{}'.format(name, ext)
     
                                          
        return os.path.join(self.path,instance.paciente_id.empresa_id.empresa_ruc,instance.dis_id.dis_nom,self.posicion,mes, filename)



''' 
def photo_file_name(self, filename):
    extension = filename.split('.')[-1]
    filename = 'cover_photo_{}.{}'.format("algo", extension)
    return os.path.join('retinopatia/eye_left/', filename)
'''
class Resumen(models.Model):
    empresa_id = models.IntegerField(blank=True, null=True)
    año = models.IntegerField(blank=True, null=True)
    mes = models.CharField(max_length=20,unique=True,verbose_name='MES_DESC')
    cantidad =models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_resumen'

    def __str__(self):
        return str(self.empresa_id)

class Resumen_est(models.Model):
    empresa_id = models.IntegerField(blank=True, null=True)
    disase =models.CharField(blank=True, null=True,max_length=25,verbose_name='Nombre de Enfermedad')
    año = models.IntegerField(blank=True, null=True)
    mes = models.CharField(blank=True, null=True ,max_length=20,verbose_name='MES_DESC')
    cantidad =models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_resumen_est'

    def __str__(self):
        return str(self.empresa_id)

class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    empresa_ruc = models.CharField(max_length=15,unique=True,verbose_name='R.U.C.')
    empresa_rs = models.CharField(max_length=100,unique=True,verbose_name='Razon Social')
    empresa_ubi = models.CharField(max_length=200,verbose_name='Ubicacion')
    empresa_tel = models.CharField(max_length=15,verbose_name='Telefono')
    empresa_mail = models.EmailField(max_length=50,unique=True,null=False,verbose_name='Email')
    empresa_web = models.CharField(null=True,max_length=75,verbose_name='Pagina Web')
    empresa_log =models.ImageField(blank='',default="",upload_to=logo_file_path)
    empresa_fech_cre = models.DateTimeField(null=True,verbose_name='Fecha de creacion')
    empresa_fech_mod = models.DateTimeField(null=True,verbose_name='Fecha de modificacion')
    empresa_est = models.BooleanField(default=True,verbose_name='Estado de la empresa')

    class Meta:
        db_table = 'tbl_empresa'

    def __str__(self):
        return str(self.empresa_id)

class Paciente(models.Model):

    DOCUMENTO_CHOICES = (
        ('DNI','DNI'),
        ('PASAPORTE','Pasaporte'),
        ('CARNET','Carnet de Extranjeria'),
        ('LIBRETA','Libreta Electoral'),
        ('COD_SIST','codigo de Sistema')
    )

    SEXO_CHOICES = (
        ('M','Masculino'),
        ('F','Femenino')
    )

    

    paciente_id = models.AutoField(primary_key=True)
    usuario_id = models.OneToOneField(User,to_field='id',on_delete=models.RESTRICT,db_column='usuario_id',verbose_name='Usuario')
    paciente_ciudad = models.CharField(max_length=50,verbose_name='ciudad')
    paciente_pais = models.CharField(max_length=50,verbose_name='pais')
    paciente_doc = models.CharField(max_length=25,choices=DOCUMENTO_CHOICES,verbose_name='Tipo Documento')
    paciente_nroDoc = models.CharField(max_length=15,unique=True,verbose_name='Nro documento')
    paciente_sex = models.CharField(max_length=50,choices=SEXO_CHOICES,verbose_name='Sexo')
    paciente_tel = models.CharField(max_length=15,verbose_name='Telefono')
    paciente_dir= models.CharField(max_length=250,verbose_name='Direccion')
    paciente_fechanac = models.DateField( null=True) 
    paciente_fech_cre = models.DateTimeField(null=True,verbose_name='Fecha de creacion')
    paciente_fech_mod = models.DateTimeField(null=True,verbose_name='Fecha de modificacion')
    paciente_est = models.BooleanField(default=True,verbose_name='Estado del paciente')


    empresa_id = models.ForeignKey(
        Empresa,to_field='empresa_id',related_name='paciente_empresa',
        on_delete=models.CASCADE,db_column='empresa_id'
    )


    class Meta:
        db_table = 'tbl_paciente'

    def __str__(self):
        return str(self.paciente_nroDoc)

class Usuario(models.Model):

    DOCUMENTO_CHOICES = (
        ('DNI','DNI'),
        ('PASAPORTE','Pasaporte'),
        ('CARNET','Carnet de Extranjeria'),
        ('LIBRETA','Libreta Electoral')
        
    )

    SEXO_CHOICES = (
        ('M','Masculino'),
        ('F','Femenino')
    )

    usu_id = models.AutoField(primary_key=True)
    usuario_id = models.OneToOneField(User,to_field='id',on_delete=models.RESTRICT,db_column='usuario_id',verbose_name='Usuario')
    usu_doc = models.CharField(max_length=25,choices=DOCUMENTO_CHOICES,verbose_name='Tipo Documento')
    usu_nroDoc = models.CharField(max_length=15,unique=True,verbose_name='Nro documento')
    usu_tel = models.CharField(max_length=15,verbose_name='Telefono')
    usu_sex = models.CharField(max_length=50,choices=SEXO_CHOICES,verbose_name='Sexo')
    cargo =   models.CharField(max_length=50,verbose_name='Cargo')
    usu_fech_cre = models.DateTimeField(null=True,verbose_name='Fecha de creacion')
    usu_fech_mod = models.DateTimeField(null=True,verbose_name='Fecha de modificacion')
    usu_est = models.BooleanField(default=True,verbose_name='Estado del usuario')

    empresa_id = models.ForeignKey(
        Empresa,to_field='empresa_id',related_name='usuario_empresa',
        on_delete=models.CASCADE,db_column='empresa_id'
    )

    class Meta:
        db_table = 'tbl_usuario'

    def __str__(self):
        return self.usu_nroDoc


class Disase(models.Model):
    dis_id = models.AutoField(primary_key=True)
    dis_nom = models.CharField(max_length=25,verbose_name='Nombre de Enfermedad')
    dis_desc = models.CharField(max_length=150,verbose_name='Descripcion de Enfermedad')
    dis_fecha_cre =models.DateTimeField(null=True,verbose_name='Fecha de creacion')
    dis_fecha_mod =models.DateTimeField(null=True,verbose_name='Fecha de modificacion')
    dis_est = models.BooleanField(default=True,verbose_name='Estado de la Enfermedad')

    class Meta:
        db_table = 'tbl_disase'

    def __str__(self):
        return str(self.dis_id)

class Diagnostico(models.Model):
    def upload_path():
        return 'photos'
    DISEASE_CHOICES = (
        ('RETINOPATIA','Retinopatia'),
        ('GLAUCOMA','Glaucoma'),
        ('CATARATAS','cataratas')
    )
    diag_id = models.AutoField(primary_key=True)
    diag_disease  = models.CharField(max_length=25,choices=DISEASE_CHOICES,verbose_name='Tipo de Enfermedad')
    #diag_img_eye_right =CloudinaryField('image1',default='')
    #diag_img_eye_left =CloudinaryField('image2',default='')

    diag_img_eye_right =models.ImageField(blank='',default="",upload_to=PathAndRename('disases','right').wrapper)   
    diag_img_eye_left =models.ImageField(blank='',default="",upload_to=PathAndRename('disases','left').wrapper )
    #diag_img_eye_right =models.ImageField(blank='',default="",upload_to='retinopatia/eye_right')   
    #diag_img_eye_left =models.ImageField(blank='',default="",upload_to='retinopatia/eye_left' )
    diag_nivel_disease_right =models.IntegerField(blank=True, null=True)
    diag_nivel_disease_left =models.IntegerField(blank=True, null=True)
    diag_nivel_disease_change_right =models.IntegerField(blank=True, null=True)
    diag_nivel_disease_change_left =models.IntegerField(blank=True, null=True)
    diag_fech_cre = models.DateTimeField(null=True,verbose_name='Fecha de creacion')
    diag_fech_mod = models.DateTimeField(null=True,verbose_name='Fecha de modificacion')
    diag_est = models.BooleanField(default=True,verbose_name='Estado del Diagnostico')
    diag_rnroDoc = models.CharField(blank=True, null=True,default="",max_length=15,verbose_name='Nro documento')

    paciente_id = models.ForeignKey(
        Paciente,to_field='paciente_id',related_name='paciente_diagnostico',
        on_delete=models.RESTRICT,db_column='paciente_id'
    )

    dis_id = models.ForeignKey( 
        Disase,to_field='dis_id',default=1,
        on_delete=models.RESTRICT,db_column='dis_id'
    )

    class Meta:
        db_table = 'tbl_diagnostico'

    def __str__(self):
        return str(self.diag_id)

 


''' 
from cloudinary.forms import CloudinaryFileField
class DiagnosticoForm(ModelForm):
    class Meta:
        model = Diagnostico
        fields = ('diag_id', 'diag_disease', 'diag_img_eye_right','paciente_id')
        diag_img_eye_right = CloudinaryFileField(options={'folder' : 'media/photos_right/', 'tags': 'landscapes'})
        diag_img_eye_left = CloudinaryFileField(options={'folder' : 'media/photos_left/', 'tags': 'landscapes'})

'''