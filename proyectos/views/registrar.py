# from django.http import JsonResponse
# from proyectos.serializers.signup import UserSignUpSerializer
# from openpyxl import load_workbook
# from django.views.decorators.csrf import csrf_exempt
# from proyectos.serializers.user import UserModelSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from proyectos.models import Perfil, Rol
# from django.contrib.auth.models import User

# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         workbook = load_workbook(file)
#         sheet = workbook.active
#         users = []
        
#         for row in sheet.iter_rows(values_only=True):
#             row_data = {
#                 'username': row[0],
#                 'email': row[1],
#                 'first_name': row[2],
#                 'last_name': row[3],
#                 'password': row[4],
#                 'password_confirmation': row[4]
#             }
            
#             serializer = UserSignUpSerializer(data=row_data)
#             serializer.is_valid(raise_exception=True)
#             user = serializer.save()                   
#             user_data = UserModelSerializer(user).data
#             rol_value = row[7]
#             try:
#                 rol_instance = Rol.objects.get(nombre=rol_value)
#                 print(rol_instance.id)
#             except Rol.DoesNotExist:
#                 # Handle the case where the role does not exist in the database
#                 # You can create a new role or raise an error depending on your requirements
#                 continue
#             user_id = user_data['id']
#             try:
#                 user_instance = User.objects.get(id=user_id)
#             except User.DoesNotExist:
#                 # Handle the case where the user does not exist in the database
#                 # You can create a new user or raise an error depending on your requirements
#                 continue

#             per = Perfil()
#             per.documento = row[6]       
#             per.rol = rol_instance
#             per.usuario = user_instance
#             per.tipo_documento = row[5]

#             # Save the profile object directly, no need for commit=False
#             per.save()
#             print(per)

#             users.append(user_data)

#         workbook.close()

#         return JsonResponse(users, safe=False)

#     return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

from django.http import JsonResponse
from proyectos.serializers.signup import UserSignUpSerializer
from django.views.decorators.csrf import csrf_exempt
from proyectos.serializers.user import UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from proyectos.models import Perfil, Rol, Ficha, Inscrito
from django.contrib.auth.models import User
from openpyxl import load_workbook
import json

# Vista para subir un archivo y procesar los datos de usuarios en él
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        # Obtener ficha_id, rol_id y el archivo del cuerpo de la solicitud POST
        ficha_id = request.POST.get('ficha_id', None)
        rol_id = request.POST.get('rol_id', None)
        file = request.FILES.get('file', None)
        print('rol', rol_id)

        # Verificar que los datos requeridos están presentes en la solicitud
        if not file or ficha_id is None or rol_id is None:
            return JsonResponse({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intentar obtener instancias de Rol y Ficha utilizando los IDs proporcionados
            rol_instance = Rol.objects.get(id=rol_id)
            ficha_instance = Ficha.objects.get(id=ficha_id)
        except Rol.DoesNotExist:
            return JsonResponse({'error': 'Invalid rol_id'}, status=status.HTTP_400_BAD_REQUEST)
        except Ficha.DoesNotExist:
            return JsonResponse({'error': 'Invalid ficha_id'}, status=status.HTTP_400_BAD_REQUEST)

        # Cargar el archivo Excel utilizando la biblioteca openpyxl
        workbook = load_workbook(file)
        sheet = workbook.active
        users = []
        skip_first_row = True  # Flag to skip the first row

        # Recorrer las filas del archivo Excel y procesar los datos de los usuarios
        for index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            if skip_first_row:
                skip_first_row = False
                continue  # Skip processing the first row
            if row[0] == None:
                break

            try:
                # Extraer los datos del usuario de la fila actual
                row_data = {
                    'username': row[0],
                    'email': row[0],
                    'first_name': row[3],
                    'last_name': row[4],
                    'password': row[1],
                    'password_confirmation': row[1]  # Suponemos que se utiliza la misma contraseña para confirmación
                }
               

                try:
                    # Validar los datos del usuario utilizando el serializador UserSignUpSerializer
                    serializer = UserSignUpSerializer(data=row_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()

                    # Crear el modelo Perfil y asignar valores a sus atributos
                    per = Perfil()
                    per.documento = row[1]
                    per.rol = rol_instance
                    per.usuario = user
                    per.tipo_documento = row[2]

                    # Guardar el modelo Perfil en la base de datos
                    per.save()

                    # Crear el modelo Inscrito y asignar valores a sus atributos
                    inscrito = Inscrito()
                    inscrito.perfil = per
                    inscrito.ficha = ficha_instance

                    # Guardar el modelo Inscrito en la base de datos
                    inscrito.save()

                    # Resto del código para perfil e inscrito...

                except Exception as e:
                    # Capturar el error (imprimirlo o usar un logger para guardar el error)
                    print(f"Error procesando Fila {index}: {str(e)}")
                    continue  # Continuar con la siguiente iteración si ocurre un error al guardar Perfil o Inscrito
                user_data = UserModelSerializer(user).data
                

                # Agregar los datos del usuario al resultado final
                users.append(user_data)

            except StopIteration:
                # Romper el bucle cuando no hay más filas en el archivo Excel
                break

        workbook.close()

        # Devolver una respuesta JSON con los datos de los usuarios registrados
        return JsonResponse(users, safe=False)

    # Devolver una respuesta de error si el método de solicitud no es POST
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


