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

        # Recorrer las filas del archivo Excel y procesar los datos de los usuarios
        for index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            try:
                # Extraer los datos del usuario de la fila actual
                row_data = {
                    'username': row[0],
                    'email': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'password': row[4],
                    'password_confirmation': row[4]  # Suponemos que se utiliza la misma contraseña para confirmación
                }

                # Imprimir los datos del usuario de la fila actual (opcional, solo para depuración)
                print(f"Row {index} Data:", row_data)

                # Verificar que no haya valores vacíos o nulos en los datos del usuario
                if any(value is None for value in row_data.values()):
                    print(f"Skipping Row {row_data} - Incomplete data.")
                    break

                # Validar los datos del usuario utilizando el serializador UserSignUpSerializer
                serializer = UserSignUpSerializer(data=row_data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user_data = UserModelSerializer(user).data
                user_id = user_data['id']

                try:
                    # Intentar obtener la instancia del usuario recién creado
                    user_instance = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return JsonResponse({'error': f'User with ID {user_id} not found'}, status=status.HTTP_400_BAD_REQUEST)

                # Crear un perfil relacionado con el usuario y la ficha
                per = Perfil()
                per.documento = row[6]
                per.rol = rol_instance
                per.usuario = user_instance
                per.tipo_documento = row[5]
                per.save()

                # Crear un registro de Inscrito relacionando el perfil con la ficha
                inscrito = Inscrito()
                inscrito.perfil = per
                inscrito.ficha = ficha_instance
                inscrito.save()

                # Imprimir los datos de los registros creados (opcional, solo para depuración)
                print(inscrito)
                print(per)

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

