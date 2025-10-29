from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    try:
        properties = get_all_properties()
        data = list(properties.values())
        return JsonResponse({"count": len(data), "results": data})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "No properties found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

