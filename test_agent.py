from agent import analyze_map_issue

result = analyze_map_issue(
    place_name="Jaipur Railway Station, Jaipur, India",
    reported_lat=26.9197,
    reported_lon=75.7878,
    problem_type="Wrong Location",
    description="Testing a reported location"
)
for key, value in result.items():
    print(f"{key}: {value}")