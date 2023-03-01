from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from rest_framework import serializers

''' 
class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.
    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268
    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
'''
'''
class Base64ImageField(serializers.ImageField):
    def from_native(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).from_native(data)
 '''
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class PacienteResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resumen
        #fields = '__all__'
        fields = ['empresa_id','año','mes','cantidad']

class PacienteResumenDisaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resumen_est
        #fields = '__all__'
        fields = ['empresa_id','año','mes','cantidad','disase']


class EmpresaSerializer(serializers.ModelSerializer):

    empresa_log = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
        model = Empresa
        #fields = '__all__'
        fields = ['empresa_id','empresa_ruc','empresa_rs','empresa_ubi','empresa_tel','empresa_log']
        #fields = ['empresa_id','empresa_ruc','empresa_log']


class DisaseSerializerget(serializers.ModelSerializer):
    class Meta:
        model = Disase
        #fields = '__all__'
        fields = ['dis_id','dis_nom']

class DisaseSerializerpost(serializers.ModelSerializer):
    class Meta:
        model = Disase
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = User(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class DiagnosticoSerializergetdni(serializers.ModelSerializer):

    class Meta:
        model = Diagnostico
        fields = ['diag_id','paciente_id']



class DiagnosticoSerializerget(serializers.ModelSerializer):

    diag_img_eye_right = Base64ImageField(max_length=None, use_url=True,)
    diag_img_eye_left = Base64ImageField(max_length=None, use_url=True,)

   
    class Meta:
        model = Diagnostico
        fields = ['diag_id','diag_disease','diag_img_eye_right','diag_img_eye_left','diag_nivel_disease_right','diag_nivel_disease_left','diag_nivel_disease_change_right','diag_nivel_disease_change_left','diag_fech_cre','diag_fech_mod','diag_est','paciente_id','diag_rnroDoc','dis_id']
        #fields = ['diag_id','diag_disease','diag_img_eye_right','diag_img_eye_left','paciente_id']


    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        serializerDisase = DisaseSerializerget(instance.dis_id)
        representation['Disase'] = serializerDisase.data

        return representation

class PacienteSerializerGETdni(serializers.ModelSerializer):

    class Meta:
        model = Paciente

        fields = ['paciente_id','paciente_nroDoc']

class PacienteSerializerGET(serializers.ModelSerializer):

    paciente_diagnostico = DiagnosticoSerializerget(many=True)
    class Meta:
        model = Paciente

        fields = ['paciente_id','paciente_doc','paciente_nroDoc','paciente_sex','paciente_tel',
         'paciente_dir','paciente_fechanac','usuario_id','empresa_id','paciente_diagnostico']



    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        serializereEmpresa = EmpresaSerializer(instance.empresa_id)
        representation['Empresa'] = serializereEmpresa.data
        serializerUsuario = UserSerializer(instance.usuario_id)
        representation['Usuario'] = serializerUsuario.data
        return representation

class UsuarioSerializerGET(serializers.ModelSerializer):

    class Meta:
        model = Usuario

        fields = ['usu_id','usu_doc','usu_nroDoc','usu_sex','cargo','empresa_id','usuario_id']



    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        serializereEmpresa = EmpresaSerializer(instance.empresa_id)
        representation['Empresa'] = serializereEmpresa.data
        serializerUsuario = UserSerializer(instance.usuario_id)
        representation['Usuario'] = serializerUsuario.data
        return representation

class DiagnosticoSerializerPost(serializers.ModelSerializer):

    diag_img_eye_right = Base64ImageField(max_length=None, use_url=True,)
    diag_img_eye_left = Base64ImageField(max_length=None, use_url=True,)


    class Meta:
        model = Diagnostico
        #fields = ['diag_id','diag_disease','diag_nivel_disease_right','diag_nivel_disease_left','diag_nivel_disease_change_right','diag_nivel_disease_change_left','diag_fech_cre','diag_fech_mod','diag_est','paciente_id','diag_rnroDoc','dis_id']
        fields = ['diag_id','diag_disease','diag_img_eye_right','diag_img_eye_left','diag_nivel_disease_right','diag_nivel_disease_left','diag_nivel_disease_change_right','diag_nivel_disease_change_left','diag_fech_cre','diag_fech_mod','diag_est','paciente_id','diag_rnroDoc','dis_id']
        
        #fields = ['diag_id','diag_disease','paciente_id','dis_id']
    ''' 
    def create(self, validated_data):
        diag_img_eye_right = validated_data.pop('diag_img_eye_right')
        created_item = Diagnostico.objects.create(**validated_data)
        created_item.diag_img_eye_right = diag_img_eye_right
        created_item.save()

        diag_img_eye_left = validated_data.pop('diag_img_eye_left')
        created_item2 = Diagnostico.objects.create(**validated_data)
        created_item2.diag_img_eye_left = diag_img_eye_left
        created_item2.save()
        return True
    '''
class DiagnosticoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnostico
        fields = ['diag_id','diag_disease','diag_nivel_disease_change_right','diag_nivel_disease_change_left',
        'diag_fech_mod','paciente_id','dis_id']

class DiagnosticoSerializerPutLeft(serializers.ModelSerializer):

    diag_img_eye_left = Base64ImageField(max_length=None, use_url=True,)
    
    class Meta:
        model = Diagnostico
        fields = ['diag_id','diag_disease','diag_img_eye_left',
        'diag_fech_mod','paciente_id','dis_id']

class DiagnosticoSerializerPutRigth(serializers.ModelSerializer):

    diag_img_eye_right = Base64ImageField(max_length=None, use_url=True,)
    
    class Meta:
        model = Diagnostico
        fields = ['diag_id','diag_disease','diag_img_eye_right',
        'diag_fech_mod','paciente_id','dis_id']
    
class MyTokenObtainPairSerializer2(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        empresa_id=Usuario.objects.get(usuario_id=user.id).empresa_id.empresa_id
        usu_nroDoc=Usuario.objects.get(usuario_id=user.id).usu_nroDoc

        print("la empresa id es: ", empresa_id)
        # Add custom claims
        token['id'] = user.id
        token['name'] = user.username
        token['empresa_id'] = empresa_id
        token['usu_nroDoc'] = usu_nroDoc

        # ...

        return token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
  
   def validate(self, attrs):
	
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        empresa_id=Usuario.objects.get(usuario_id=self.user.id).empresa_id.empresa_id
        empresa_rs=Usuario.objects.get(usuario_id=self.user.id).empresa_id.empresa_rs
        usu_nroDoc=Usuario.objects.get(usuario_id=self.user.id).usu_nroDoc
                    
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        #data['id'] = user.id
        #data['name'] = user.username
        data['empresa_id'] = empresa_id
        data['usu_nroDoc'] = usu_nroDoc
        data['empresa_rs'] = empresa_rs

        return data
			
              