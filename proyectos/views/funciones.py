from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User 
from proyectos.models import Entrega, Proyecto, Inscrito, Perfil



def perfil_conectado(user_id):
    """
    Obtiene el ID del perfil conectado a un usuario.

    Args:
        user_id (int): El ID del usuario.

    Returns:
        int: El ID del perfil conectado al usuario.

    Raises:
        Http404: Si no se encuentra el usuario o el perfil correspondiente.
    """
    user = get_object_or_404(User, id=user_id)
    perfil = get_object_or_404(Perfil, usuario=user)
    return perfil.id

