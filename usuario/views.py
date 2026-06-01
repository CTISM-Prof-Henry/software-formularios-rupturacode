from django.http import JsonResponse


def usuario_status(request):
    return JsonResponse({"detail": "Modulo de usuarios disponivel apenas via API."})
