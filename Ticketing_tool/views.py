from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "OK",
        "service": "Ticketing Tool Backend Running ✅"
    }, status=200)
