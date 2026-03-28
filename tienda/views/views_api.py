import random
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pasarela_pago(request):
    """
    Simula una pasarela de pago externa.
    70% confirmado, 30% rechazado.
    """
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            monto = datos.get('monto', 0)
            pedido_id = datos.get('pedido_id')

            resultado = random.choices(
                ['confirmado', 'rechazado'],
                weights=[70, 30]
            )[0]

            if resultado == 'confirmado':
                return JsonResponse({
                    'estado': 'confirmado',
                    'mensaje': 'Pago procesado exitosamente',
                    'pedido_id': pedido_id,
                    'monto': monto,
                    'codigo_transaccion': f'TXN-{random.randint(100000, 999999)}'
                }, status=200)
            else:
                return JsonResponse({
                    'estado': 'rechazado',
                    'mensaje': 'Pago rechazado por el banco',
                    'pedido_id': pedido_id,
                    'monto': monto,
                }, status=200)

        except Exception as e:
            return JsonResponse({
                'estado': 'error',
                'mensaje': str(e)
            }, status=400)

    return JsonResponse({'estado': 'error', 'mensaje': 'Método no permitido'}, status=405)