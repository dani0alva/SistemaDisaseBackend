from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('',views.indexView.as_view()),
    path('paciente',views.PacienteView.as_view()),
    path('pacientefiltro/<int:paciente_id>',views.EmpresaViewFiltro.as_view()),
    
    path('pacientedetail/<int:empresa_id>',views.PacienteDetailView.as_view()),
    path('pacienteDisaseResumen/<int:empresa_id>',views.PacienteResumenDisaseView.as_view()),
    path('pacienteResumen/<int:empresa_id>',views.PacienteResumenView.as_view()),
    path('pacientefiltrodni/<int:paciente_nroDoc>',views.PacienteViewFiltroDNI.as_view()),
    
    
    path('UsuarioDetail',views.UsuarioDetailView.as_view()),
    
    path('empresa/',views.EmpresaView.as_view()),
    path('empresadetail/<int:empresa_id>',views.EmpresaViewDetail.as_view()),

    path('diagnostico/',views.DiagnosticoView.as_view()),
    path('diagnosticodetail/<int:diag_id>',views.DiagnosticoViewDetail.as_view()),
    path('diagnosticodetaildniexist/<int:paciente_nroDoc>',views.DiagnosticoDNIViewDetailExist.as_view()),
    path('diagnosticodetaildni/<int:paciente_nroDoc>',views.DiagnosticoDNIViewDetail.as_view()),

    path('disase/',views.DisaseView.as_view()),
    
    
    path('user/create/',views.CustomUserCreate.as_view()),
    path('token/obtain/', views.ObtainTokenPairWithColorView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path('blacklist/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist')
]