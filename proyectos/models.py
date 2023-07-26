from django.db import models
from django.contrib.auth.models import User 

from django.core.validators import RegexValidator


# Create your models here.
MODALIDAD = (
    ('presencial', 'Presencial'),
    ('virtual', 'Virtual'),
)

ROL = (
    ('aprendiz', 'Aprendiz'),
    ('instructor', 'Instructor'),
    ('admin', 'Admin'),
    ('anonimo', 'Anonimo'),
)
TIPO_DOCUMENTO = (
    ('CC', 'CC'),
    ('TI', 'TI'),
    ('CE', 'CE'),
    ('PASAPORTE', 'PASAPORTE'),
)

CALIFICACION = (
    ('en revision', 'en revision'),
    ('aprobado', 'Aprobado'),
    ('No aprobado', 'No aprobado'),
)
    
ESTADO_PROYECTO = (
    
    ('terminado', 'terminado'),
    ('en revision', 'en revision'),
    ('en desarrollo', 'en desarrollo'),
    ('anulado', 'anulado'),
    ('en correccion',  'en correcion')
    #
    # agragar otro estado
)
#inscrito
ESTADO_GRUPO = (
    ('activo','activo'),
    ('inactivo','inactivo'),
    ('abandono_grupo_proyecto','abandono_grupo_proyecto'),
)

class Regional (models.Model):
    nombre          =models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.nombre

class Centros_de_formacion(models.Model):
    nombre          =models.CharField(max_length=300, unique=True)
    direccion       =models.CharField(max_length=100,null= True, blank= True )
    encargado       =models.CharField(max_length=20,null= True, blank= True)
    regional        =models.ForeignKey(Regional, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre + " " + self.regional.nombre
    
class Programa(models.Model):
    nombre               = models.CharField(max_length=300,unique=True)
    centros_de_formacion = models.ForeignKey(Centros_de_formacion, on_delete=models.PROTECT) 
    # Centros de formacion tiene una relacion de UNO a MUCHOS con Programa
       
    def __str__(self):
        return self.nombre


class Ficha(models.Model):

    codigo              = models.PositiveIntegerField(unique=True) 
    fecha_inicio        = models.DateField()
    fecha_finalizacion  = models.DateField()
    modalidad           = models.CharField(max_length=12, choices = MODALIDAD, default='presencial') # Presencial o Virtual
    programa            = models.ForeignKey(Programa, on_delete = models.PROTECT) 
    # Programa tiene una relacion de uno a muchos con Ficha(programa)
    
    def __str__(self):
        return str(self.codigo) + " " + self.programa.nombre

# class User(AbstractUser):
#     #extender desde el usuario de Abtract de django,
#     # cambiar el campo de nombre de usuario a correo electrónico agregar algunos campos adicionales

#     email = models.EmailField(
#         'email address',
#         unique=True,
#         # Error_messsages={
#         #     'unique': 'Ya existe un usuario con ese email'
#         # }
#     )
#     # phone_regex = RegexValidator(
#     #     regex=r'\+'?1?\d{9,15}$',
#     #     message="El número de teléfono debe ingresarse en el formato: +999999999. Se permiten hasta 15 dígitos".
#     # )
#     # phone_number = models.CharField(validators=[phone_regex],max_length=17, blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS =['username','first_name', 'last_name']

#     # is_client = models.Booleanfield(
#     #     'client status'
#     #     default=True,
#     #     help_text=(
#     #         ' ayudar a distinguir fácilmente a los usuarios y realizar consultas.'
#     #         'Los clientes son los principales usuarios .'
#     #     )
#     # )
#     # is_verified = models.BooleanField(
#     #     'verifield',
#     #     default=True,
#     #     help_text=' Establecido en verdadero cuando el usuario haya verificado su dirección de correo electrónico.'
#     # )
#     def __str__(self):
#         """Return username"""
#         return self.username

#     # def get_short_name(self):
#     #     return self.username


class Rol(models.Model):
    nombre  = models.CharField(max_length=30, choices=ROL, unique=True)
    
    def __str__(self):
        return str(self.id) + " " + self.nombre

class Perfil(models.Model):
    """perfil model

    Un perfil contiene datos públicos de un usuario como:
    documento, tipo documento, direccion , foto ...
    """
    documento       = models.PositiveIntegerField(unique=True)
    tipo_documento  = models.CharField(max_length=20, choices = TIPO_DOCUMENTO)
    direccion       = models.CharField(max_length=50,null= True, blank= True)
    telefono        = models.CharField(max_length=15,null= True, blank= True)
    foto            = models.ImageField(upload_to='perfiles', null=True, blank=True)
    web             = models.URLField(null= True, blank= True,)
    rol             = models.ForeignKey(Rol,on_delete = models.PROTECT)
    usuario         = models.OneToOneField(User, on_delete = models.CASCADE)
    creado          = models.DateTimeField(auto_now_add = True)
    editado         = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.usuario.username

    
class Tipo_Revision(models.Model):
    nombre      = models.CharField(max_length=200, unique = True)

    def __str__(self):
        return self.nombre

class Categoria (models.Model):  
    nombre      = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre
    
class Grupo (models.Model):
    nombre_grupo    = models.CharField(max_length=15, unique = True) # c+odigo auto generado por medio de un script 

    def __str__(self):
        return self.nombre_grupo

class Inscrito (models.Model):
    # estado del aprendiz respecto a la ficha
    estado        = models.CharField(max_length=30,choices=ESTADO_GRUPO, default='activo')
    nombre_grupo  = models.ForeignKey(Grupo, null=True, blank=True, on_delete = models.PROTECT )
    perfil        = models.ForeignKey(Perfil, on_delete = models.PROTECT)
    ficha         = models.ForeignKey(Ficha, on_delete = models.PROTECT)
    # proyecto        = models.IntegerField(null= True, blank= True) # consulta el id del Proyecto
    
    def __str__(self):
        return str(self.perfil)
    
class Proyecto(models.Model):

    nombre_proyecto     = models.CharField(max_length=300 )    
    descripcion         = models.CharField(max_length=5000 )    
    foto                = models.ImageField(upload_to='proyectos/foto', null=True, blank=True)
    aprendiz                = models.ForeignKey(Inscrito, on_delete=models.CASCADE)
    codigo_fuente       = models.URLField(null= True, blank= True,)    
    categorias          = models.ManyToManyField(Categoria, null=True, blank=True)

    # documento       = models.FileField(upload_to = 'proyectos/documentos', null=True, blank=True)  # documento inicial del anteproyecto  
    estado              = models.CharField(max_length=20, choices = ESTADO_PROYECTO, default = 'en revision')
    calificacion         = models.CharField(max_length=15,null= True, blank= True,)

    creado              = models.DateTimeField(auto_now_add = True)
    editado             = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.nombre_proyecto




class Entrega (models.Model):
    calificacion            = models.CharField(max_length=20, choices = CALIFICACION,default = 'en revision',null= True, blank= True)
    descripcion_entrega     = models.CharField(max_length=5000 )    
    respuesta_instructor    = models.CharField(max_length=5000, null= True, blank= True)  
    # Estado_entrega          = models.CharField(max_length=5000 )   
    instructor              = models.CharField(max_length=300 ,null= True, blank= True) # solo va el nombre del instructor que hizo la revision      
    proyecto                = models.ForeignKey(Proyecto, on_delete = models.PROTECT )
    tipo_revision           = models.ForeignKey(Tipo_Revision, on_delete = models.PROTECT)
    # aprendiz                = models.ForeignKey(Inscrito, on_delete=models.CASCADE)
    autor                   = models.CharField(max_length=300 ,null= True, blank= True)
    creado                  = models.DateTimeField(auto_now_add = True)
    editado                 = models.DateTimeField(auto_now = True)
    documento               = models.FileField(upload_to = 'entrega/documento',null= True, blank= True)
    url                     = models.URLField(null= True, blank= True,)    

    def __str__(self):
        return self.calificacion + " " + str(self.creado) + " " + str(self.editado)
    


