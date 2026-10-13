import math


def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371000
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return earth_radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def detect_location_error(
    reported_lat,
    reported_lon,
    reference_lat,
    reference_lon,
    threshold_meters=100,
):
    distance = calculate_distance(
        reported_lat, reported_lon, reference_lat, reference_lon
    )
    return {
        "distance_meters": round(distance, 2),
        "possible_error": distance > threshold_meters,
        "threshold_meters": threshold_meters,
    }
