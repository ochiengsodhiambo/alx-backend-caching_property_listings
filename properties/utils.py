from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        print("Cache MISS — fetching from DB")
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    else:
        print("Cache HIT — using cached data")
    return properties


def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    }
    print(metrics)
    return metrics
