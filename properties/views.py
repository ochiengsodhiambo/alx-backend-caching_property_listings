from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties  # we'll create this next

@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    data = list(properties.values())
    return JsonResponse(data, safe=False)
