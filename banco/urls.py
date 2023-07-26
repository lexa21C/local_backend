"""Banco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#django
from django.contrib import admin
from django.urls import path, include
# proyecto fichas 
from  proyectos.views.fichas.fichas_de_usuario import FichasDeUsuarioViewSet
from  proyectos.views.fichas.integrantes import FichaIntegrantesViewSet
#proyectos aprendiz
from proyectos.views.aprendiz.proyectos_aprendiz import ProyectosAprendizViewSet
from proyectos.views.aprendiz.grupos import UsuarioGruposViewSet
from proyectos.views.aprendiz.grupo_proyecto import GrupoProyectosViewSet
from proyectos.views.registrar import upload_file

#proyectos grupos
from proyectos.views.grupos.agregar_integrantes import AgregarInscritosViewSet
from proyectos.views.grupos.integrantes import IntegrantesViewSet
#proyectos instructor
from proyectos.views.instructor.calificar_proyecto import CalificaProyectoViewSet
from proyectos.views.instructor.proyectos_instructor import ProyectosInstructorViewSet
#usuario
from proyectos.views.login import UserLoginAPIView
from proyectos.views.signup import UserSignUpAPIView
# Proyectos
from proyectos.views.proyectos.proyecto_entregas import ProyectoEntregasViewSet
from proyectos.views.proyectos.participantes import ProyectoParticpantesViewSet
from proyectos.views.proyectos.buscar_proyectos import BuscarProyectos



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('proyectos.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login/', UserLoginAPIView.as_view(), name='login'),
    path('api/signup/', UserSignUpAPIView.as_view(), name='signup'),
     path('api/upload/', upload_file, name='upload_file'),
    #fichas
    path('api/fichas-usuario/<int:user_id>/', FichasDeUsuarioViewSet.as_view({'get':'get_fichas'}),name='fichas_de_un_usuario'),
    path('api/fichas-integrantes/<int:ficha_id>/', FichaIntegrantesViewSet.as_view({'get':'get_ficha_inscritos'}),name='integrantes_inscritos_a_una_ficha '),
    #aprendiz
    path('api/proyectos-aprendiz/<int:user_id>/',ProyectosAprendizViewSet.as_view({'get':'get_proyectos_aprendiz'}), name='proyectos_asociados_a_un_aprendiz '),
    path('api/usuario-grupos/<int:user_id>/', UsuarioGruposViewSet.as_view({'get': 'get_mis_grupos'}), name='lista_de_grupos_de un_usuario'),
    path('api/grupo-proyecto/<int:user_id>/', GrupoProyectosViewSet.as_view({'get': 'get_mis_grupos'}), name='grupo_asociado_al_proyecto'),
    #grupos
    path('api/agregar-integrantes/<int:id_user>/', AgregarInscritosViewSet.as_view({'get': 'get_inscritos'}), name='agregar_inscritos'),#terminado
    path('api/integrantes/<int:grupo_id>/', IntegrantesViewSet.as_view({'get': 'get_integrantes'}), name='get_fichas_usuario'),
    # instructor
    path('api/calificar-proyecto/<int:proyecto_id>/<str:estado>/', CalificaProyectoViewSet.as_view({'put': 'actualizar_proyecto'}), name='calificar_proyecto'),#terminado
    path('api/proyectos-instructor/<int:ficha_id>/', ProyectosInstructorViewSet.as_view({'get':'get_proyectos_instructor'}),name='proyectos_asociados_a_una_ficha '),
    # Proyecto
    path('buscar_proyectos/', BuscarProyectos.as_view()),
    path('api/proyecto-entregas/<int:id_proyecto>/', ProyectoEntregasViewSet.as_view({'get': 'get_entregas_por_proyecto'}), name='lista_entregas_por_proyecto'),#terminado
    path('api/proyecto-participantes/<int:proyecto_id>/', ProyectoParticpantesViewSet.as_view({'get':'get_participantes'}), name='participantes_del_proyecto'),#terminado
   

]

