from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

def get_all_properties():
    """Retrieve all properties, using Redis cache if available."""
    properties = cache.get('all_properties')
    if not properties:
        print("Cache MISS — fetching from DB")
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    else:
        print("Cache HIT — using cached data")
    return properties


def get_redis_cache_metrics():
    """Return Redis cache hit/miss metrics and hit ratio."""
    try:
        conn = get_redis_connection("default")
        info = conn.info()
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2)
        }
        print(metrics)
        return metrics
    except Exception as e:
        print(f"Error retrieving Redis metrics: {e}")
        return {"error": str(e)}
