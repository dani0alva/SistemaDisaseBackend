
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication ,TokenAuthentication
 
from .models import *
from .serializers import *
from datetime import datetime
import cloudinary
import cloudinary.uploader

class indexView(APIView):

    permission_classes = (IsAuthenticated,)
    #permission_classes = [permissions.IsAuthenticated]

    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,
     #               IsOwnerOrReadOnly]
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        context = {
            'status' : True,
            'content' : 'API activo'
        }

        return Response(context)
class PacienteView(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data = Paciente.objects.all()
        serializerData = PacienteSerializer(data,many=True)

        context = {
            'content':serializerData.data
        }

        return Response(serializerData.data)


class EmpresaViewFiltro(APIView):
    ''' 
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    '''
    permission_classes = (IsAuthenticated,)

    def get(self,request, paciente_id):

        try: 
            paciente = Paciente.objects.get(pk=paciente_id) 
        except Paciente.DoesNotExist: 
            return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

        if request.method == 'GET': 
            paciente_serializer = PacienteSerializerGET(paciente) 
            return Response(paciente_serializer.data) 
    
class PacienteViewFiltroDNI(APIView):
  
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    
    #permission_classes = (IsAuthenticated,)

    def get(self,request, paciente_nroDoc):

        print("el nero de doc del pacientes es:",paciente_nroDoc)
        try: 
            paciente = Paciente.objects.get(paciente_nroDoc=paciente_nroDoc) 
        except Paciente.DoesNotExist: 
            return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

        if request.method == 'GET': 
            paciente_serializer = PacienteSerializerGETdni(paciente) 
            return Response(paciente_serializer.data)    


class PacienteDetailView(APIView):
   #authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
   #authentication_classes = [TokenAuthentication]
   #permission_classes = [IsAuthenticated]
   # def get(self,request,turista_id):
   #     data = Paciente.objects.get(pk=turista_id)
   #     serializerData = PacienteSerializer(data)

   #     context = {
   #         'content':serializerData.data
   #     }

   #     return Response(serializerData.data)

   permission_classes = (IsAuthenticated,)
   def get(self,request,empresa_id):

        empresa = Empresa.objects.get(pk=empresa_id)

        data = Paciente.objects.filter(empresa_id=empresa)

      #  data = Paciente.objects.all()
        serializerData = PacienteSerializerGET(data,many=True)

        context = {
            'content':serializerData.data
        }

        return Response(serializerData.data)


class PacienteResumenDisaseView(APIView):
   #authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
   #authentication_classes = [TokenAuthentication]
   #permission_classes = [IsAuthenticated]
   permission_classes = (IsAuthenticated,)
   def get(self,request,empresa_id):

            data = Resumen_est.objects.raw('''SELECT 1 as id,
                                            c.dis_nom as disase,
                                            b.empresa_id as empresa_id,
                                            YEAR(diag_fech_cre) AS año,
                                            case 
                                            when MONTH(diag_fech_cre)=1 then 'ENERO'
                                            when MONTH(diag_fech_cre)=2 then 'FEBRERO'
                                            when MONTH(diag_fech_cre)=3 then 'MARZO'
                                            when MONTH(diag_fech_cre)=4 then 'ABRIL'
                                            when MONTH(diag_fech_cre)=5 then 'MAYO'
                                            when MONTH(diag_fech_cre)=6 then 'JUNIO'

                                            when MONTH(diag_fech_cre)=7 then 'JULIO'
                                            when MONTH(diag_fech_cre)=8 then 'AGOSTO'
                                            when MONTH(diag_fech_cre)=9 then 'SETIEMBRE'
                                            when MONTH(diag_fech_cre)=10 then 'OCTUBRE'
                                            when MONTH(diag_fech_cre)=11 then 'NOVIEMBRE'
                                            when MONTH(diag_fech_cre)=12 then 'DICIEMBRE'
                                            ELSE  ''
                                            END
                                            AS mes,

                                            COUNT(1) as cantidad FROM tbl_diagnostico a left JOIN tbl_paciente  b on a.paciente_id=b.paciente_id
                                            left join tbl_disase c on a.dis_id =c.dis_id     WHERE diag_fech_cre is not null and  DATEDIFF(NOW(),diag_fech_cre)<=365 and b.empresa_id = %s
                                            GROUP BY c.dis_nom,b.empresa_id,YEAR(diag_fech_cre),MONTH(diag_fech_cre) ''', [empresa_id])

           
            serializerData = PacienteResumenDisaseSerializer(data,many=True)

            print("la data es : ",serializerData.data)
            context = {
                'content':serializerData.data
            }


            return Response(serializerData.data)

class PacienteResumenView(APIView):
   #authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
   #authentication_classes = [TokenAuthentication]
   #permission_classes = [IsAuthenticated]
    
   permission_classes = (IsAuthenticated,)

   def get(self,request,empresa_id):

            data = Resumen.objects.raw('''SELECT 1 as id,
                                            b.empresa_id as empresa_id,
                                            YEAR(diag_fech_cre) AS año,
                                            case 
                                            when MONTH(diag_fech_cre)=1 then 'ENERO'
                                            when MONTH(diag_fech_cre)=2 then 'FEBRERO'
                                            when MONTH(diag_fech_cre)=3 then 'MARZO'
                                            when MONTH(diag_fech_cre)=4 then 'ABRIL'
                                            when MONTH(diag_fech_cre)=5 then 'MAYO'
                                            when MONTH(diag_fech_cre)=6 then 'JUNIO'

                                            when MONTH(diag_fech_cre)=7 then 'JULIO'
                                            when MONTH(diag_fech_cre)=8 then 'AGOSTO'
                                            when MONTH(diag_fech_cre)=9 then 'SETIEMBRE'
                                            when MONTH(diag_fech_cre)=10 then 'OCTUBRE'
                                            when MONTH(diag_fech_cre)=11 then 'NOVIEMBRE'
                                            when MONTH(diag_fech_cre)=12 then 'DICIEMBRE'
                                            ELSE  ''
                                            END
                                            AS mes,

                                            COUNT(1) as cantidad FROM tbl_diagnostico a left JOIN tbl_paciente  b on a.paciente_id=b.paciente_id
                                            WHERE diag_fech_cre is not null and  DATEDIFF(NOW(),diag_fech_cre)<=365 and b.empresa_id = %s
                                            GROUP BY b.empresa_id,YEAR(diag_fech_cre),MONTH(diag_fech_cre) ''', [empresa_id])

           
            serializerData = PacienteResumenDisaseSerializer(data,many=True)

            print("la data es : ",serializerData.data)
            context = {
                'content':serializerData.data
            }


            return Response(serializerData.data)


class UsuarioDetailView(APIView):
    
   permission_classes = (IsAuthenticated,)

   def get(self,request):
        data = Usuario.objects.all()
        serializerData = UsuarioSerializerGET(data,many=True)

        context = {
            'content':serializerData.data
        }

        return Response(serializerData.data)

class EmpresaView(APIView):

    permission_classes = (IsAuthenticated,)
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()
    
    def get(self, request):
        data = Empresa.objects.all()
        serializerData = EmpresaSerializer(data,many=True)

        context = {
            'content':serializerData.data
        }
        
        return Response(serializerData.data)
    
    

    def post(self,request):

      
      if request.method == 'POST':
        serializerData = EmpresaSerializer(data=request.data)

        if serializerData.is_valid():
            try:
                
                serializerData.save()

                context = {
                    'ok':True,
                    'content':serializerData.data
                }

                return Response(data=context,status=status.HTTP_200_OK)
                
            except Exception as error:
                return Response(data={'message':'error en el servidor'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'message':'data es invalida'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
class EmpresaViewDetail(APIView):

    #permission_classes = (IsAuthenticated,)
 
    def get(self,request, empresa_id):

        try: 
            empresa = Empresa.objects.get(pk=empresa_id) 
        except Empresa.DoesNotExist: 
            return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

        if request.method == 'GET': 
            empresa_serializer = EmpresaSerializer(empresa) 
            return Response(empresa_serializer.data) 
    
    def put(self,request, diag_id):

        try: 
            empresa = Empresa.objects.get(pk=diag_id) 
        except Empresa.DoesNotExist: 
            return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

        if request.method == 'PUT': 
            empresa_data = request.data
            empresa_serializer = DiagnosticoSerializer(empresa, data=empresa_data) 
            if empresa_serializer.is_valid(): 
                empresa_serializer.save() 
                return Response(empresa_serializer.data) 
            return Response(empresa_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class CustomUserCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        print("--",serializer)
        print("--",request.data)

        #guardarTurista = Turista.objects.get(usuario = request.data)
 
        if serializer.is_valid():
            user = serializer.save()

            try:
                if(request.data['registro']==1):
                    guardarEmpres = Usuario(usuario_id=user,
                    
                    empresa_id = Empresa.objects.get(pk=request.data['empresa_id']),
                    
                    usu_doc=request.data['tipo_doc'],usu_nroDoc=request.data['nero_doc'],usu_tel=request.data['telefono'],usu_sex=request.data['sexo'],cargo=request.data['cargo'],
                    usu_fech_cre=datetime.today(),usu_fech_mod = datetime.today()
                    ).save()
                else:

                    guardarPaciente = Paciente(usuario_id=user,

                    empresa_id = Empresa.objects.get(pk=request.data['empresa_id']),

                    paciente_ciudad=request.data['ciudad'],paciente_pais=request.data['pais'],
                    paciente_doc=request.data['tipo_doc'],paciente_nroDoc=request.data['nero_doc'],paciente_tel=request.data['telefono'],paciente_sex=request.data['sexo'],paciente_fechanac=request.data['fecha_nac'],
                    paciente_dir="calle sin numero",paciente_fech_cre=datetime.today(),paciente_fech_mod = datetime.today()
                    ).save()
            except Exception as error:
                try: 
                    usuario = User.objects.get(username=request.data['username']) 
                    usuario.delete()
                except Diagnostico.DoesNotExist: 
                    return Response({'message': 'The diagnostico does not exist'}, status=status.HTTP_404_NOT_FOUND) 

                return Response(data={'message':'error al insertar usuario'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisaseView(APIView):
    permission_classes = (IsAuthenticated,)
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()

    def get(self,request):
     if request.method == 'GET':
        data = Disase.objects.all()
        serializerData = DisaseSerializerget(data,many=True)

        context = {
            'ok':True,
            'content':serializerData.data
        }

        return Response(serializerData.data)

     
    def post(self,request): 
      if request.method == 'POST':
        
        serializerData = DisaseSerializerpost(data=request.data)
        
        if serializerData.is_valid():
          
            serializerData.save()
           
            return Response(serializerData.data, status=status.HTTP_201_CREATED) 
        return Response(serializerData.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(0, status=status.HTTP_400_BAD_REQUEST)

class DiagnosticoDNIViewDetailExist(APIView):
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()

    permission_classes = (IsAuthenticated,)

    def get(self,request, paciente_nroDoc):
        cant_diag=0
        try: 
           
            paciente =Paciente.objects.get(paciente_nroDoc=paciente_nroDoc)
            
            cant_diag = Diagnostico.objects.filter(paciente_id=paciente).count()
            print("la cantidad de diagnostico es: ",cant_diag,)
            
        except Paciente.DoesNotExist: 
            cant_diag=-1
            return Response(cant_diag)  
            

        if request.method == 'GET': 

            #diagnostico_serializer = DiagnosticoSerializergetdni(diagnostico,many=True) 
            return Response(cant_diag) 

class DiagnosticoDNIViewDetail(APIView):
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()

    permission_classes = (IsAuthenticated,)

    def get(self,request, paciente_nroDoc):
        
        try: 
           
            paciente =Paciente.objects.get(paciente_nroDoc=paciente_nroDoc)
            
            diagnostico = Diagnostico.objects.filter(paciente_id=paciente)
            
        except Paciente.DoesNotExist: 
            return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
            

        if request.method == 'GET': 

            diagnostico_serializer = DiagnosticoSerializergetdni(diagnostico,many=True) 
            return Response(diagnostico_serializer.data) 



class DiagnosticoView(APIView):
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()

    permission_classes = (IsAuthenticated,)

    def get(self,request):
     if request.method == 'GET':
        data = Diagnostico.objects.all()
        serializerData = DiagnosticoSerializerget(data,many=True)

        context = {
            'ok':True,
            'content':serializerData.data
        }

        return Response(serializerData.data)

     
    def post(self,request): 
      if request.method == 'POST':
        print("entro antes del  serializer")
        
        serializerData = DiagnosticoSerializerPost(data=request.data)

        print("el serializer es :",request.data)
        
        if serializerData.is_valid():
            
            print("entro al validador")
            
            #para guardar de forma directa
            
            serializerData.save()
           
            return Response(serializerData.data, status=status.HTTP_201_CREATED) 
        return Response(serializerData.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(0, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
      if request.method == 'DELETE':
        count = Diagnostico.objects.all().delete()
        return Response({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
     

class DiagnosticoViewDetail(APIView):

    permission_classes = (IsAuthenticated,)
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()
 
    def get(self,request, diag_id):

        try: 
            diagnostico = Diagnostico.objects.get(pk=diag_id) 
        except Diagnostico.DoesNotExist: 
            return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

        if request.method == 'GET': 
            diagnostico_serializer = DiagnosticoSerializer(diagnostico) 
            return Response(diagnostico_serializer.data) 
    
    def put(self,request, diag_id):

        try: 
            diagnostico = Diagnostico.objects.get(pk=diag_id) 
        except Diagnostico.DoesNotExist: 
            return Response({'message': 'No existe el diagnostico'}, status=status.HTTP_404_NOT_FOUND) 
 

        if request.method == 'PUT': 
          try:

            print("entro al put")
            diagnostico_data = request.data
            if(request.data['posicion']=="left"):
                print("entro al put left")

                #cloudinary.uploader.destroy(diagnostico.diag_img_eye_left.public_id,invalidate=True)
                diagnostico_serializer = DiagnosticoSerializerPutLeft(diagnostico, data=diagnostico_data) 

            else:
                print("entro al put rigth")
                
                #cloudinary.uploader.destroy(diagnostico.diag_img_eye_right.public_id,invalidate=True)
                diagnostico_serializer = DiagnosticoSerializerPutRigth(diagnostico, data=diagnostico_data) 

            

            if diagnostico_serializer.is_valid(): 
                diagnostico_serializer.save() 
                return Response(diagnostico_serializer.data) 
            return Response(diagnostico_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
          
          except Exception as error:
                
                return Response(data={'message':'error al actualizar'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request, diag_id):

        try: 
            diagnostico = Diagnostico.objects.get(pk=diag_id) 
        except Diagnostico.DoesNotExist: 
            return Response({'message': 'The diagnostico does not exist'}, status=status.HTTP_404_NOT_FOUND) 

        if request.method == 'DELETE': 
            diagnostico.delete() 
            return Response({'message': 'diagnostico was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
