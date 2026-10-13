from detector import detect_location_error
from map_tools import search_location


def analyze_map_issue(
    place_name,
    reported_lat,
    reported_lon,
    problem_type="Wrong Location",
    description=""
):
    """
    MapGuard AI backend agent.

    Searches OpenStreetMap for the place, compares coordinates,
    and returns an analysis with a recommendation.
    """

    # Step 1: Validate the input coordinates
    if not (-90 <= reported_lat <= 90):
        return {
            "success": False,
            "error": "Reported latitude must be between -90 and 90."
        }

    if not (-180 <= reported_lon <= 180):
        return {
            "success": False,
            "error": "Reported longitude must be between -180 and 180."
        }

    if not place_name or not place_name.strip():
        return {
            "success": False,
            "error": "Please enter a location name."
        }

    # Step 2: Find the reference location
    reference = search_location(place_name)

    if not reference["success"]:
        return {
            "success": False,
            "error": reference.get(
                "error",
                "Could not find the reference location."
            )
        }

    reference_lat = reference["latitude"]
    reference_lon = reference["longitude"]

    # Step 3: Detect a possible coordinate mismatch
    detection = detect_location_error(
        reported_lat=reported_lat,
        reported_lon=reported_lon,
        reference_lat=reference_lat,
        reference_lon=reference_lon
    )

    distance = detection["distance_meters"]

    # Step 4: Analyze the reported issue
    if problem_type == "Wrong Location":

        if distance > 100:
            status = "Possible Location Error"
            confidence = 90
            recommendation = (
                "The reported coordinates are more than 100 meters "
                "from the searched reference location. Verify the "
                "intended place before correcting the map."
            )

        elif distance > 30:
            status = "Location Needs Review"
            confidence = 75
            recommendation = (
                "The coordinates differ moderately from the reference. "
                "Check the address and exact location before editing."
            )

        else:
            status = "No Major Coordinate Mismatch"
            confidence = 65
            recommendation = (
                "The coordinates are relatively close to the reference. "
                "Verify the exact entrance or intended location."
            )

    elif problem_type == "Missing Road":

        status = "Road Requires Verification"
        confidence = 50
        recommendation = (
            "Check current map data and reliable local evidence "
            "to determine whether the road is missing."
        )

    elif problem_type == "Duplicate Place":

        status = "Possible Duplicate"
        confidence = 50
        recommendation = (
            "Compare the place name, address and coordinates with "
            "existing map entries before merging anything."
        )

    elif problem_type == "Wrong Road Name":

        status = "Road Name Requires Verification"
        confidence = 50
        recommendation = (
            "Compare the reported road name with an authoritative "
            "source before recommending a name correction."
        )

    elif problem_type == "Closed Business":

        status = "Business Status Requires Verification"
        confidence = 50
        recommendation = (
            "Verify the business's current operating status before "
            "recommending a map update."
        )

    else:

        status = "Manual Review Required"
        confidence = 40
        recommendation = (
            "Collect additional evidence about the reported issue "
            "before recommending a correction."
        )

    # Step 5: Return the result to the frontend
    return {
        "success": True,
        "place_name": reference["name"],
        "reported_latitude": reported_lat,
        "reported_longitude": reported_lon,
        "reference_latitude": reference_lat,
        "reference_longitude": reference_lon,
        "distance_meters": distance,
        "possible_error": detection["possible_error"],
        "status": status,
        "confidence": confidence,
        "recommendation": recommendation,
        "description": description,
        "source": "OpenStreetMap Nominatim",
        "note": (
            "This is a rule-based prototype, not a trained AI model. "
            "The confidence score is a heuristic, not a validated "
            "probability. Verify findings before changing map data."
        )
    }

