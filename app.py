import streamlit as st
import folium
from streamlit_folium import st_folium

from agent import analyze_map_issue


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="MapGuard AI",
    page_icon="🗺️",
    layout="wide"
)


# ---------------- HEADER ----------------

st.title("🗺️ MapGuard AI")
st.subheader("Intelligent Digital Map Error Detection")
st.write(
    "Report a possible map error, compare coordinates, "
    "and review a correction recommendation."
)

st.divider()


# ---------------- SIDEBAR ----------------

st.sidebar.title("MapGuard AI")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Report Map Error", "About"]
)


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Project", "MapGuard AI")
    col2.metric("Analysis Mode", "Rule-based")
    col3.metric("Human Review", "Required")

    st.info(
        "Open 'Report Map Error' in the sidebar to test "
        "a location using the backend agent."
    )


# ---------------- REPORT MAP ERROR ----------------

elif page == "Report Map Error":

    st.header("Report a Map Error")

    st.write(
        "Enter the place name and the coordinates currently "
        "shown on your map. The backend will search for a "
        "reference location and compare the coordinates."
    )

    with st.form("map_error_form"):

        # Define the place name
        place_name = st.text_input(
            "Place name",
            value="Jaipur Railway Station, Jaipur, India",
            help="Enter a specific place, address, or landmark."
        )

        problem_type = st.selectbox(
            "Type of map error",
            [
                "Wrong Location",
                "Missing Road",
                "Duplicate Place",
                "Wrong Road Name",
                "Closed Business",
                "Other"
            ]
        )

        description = st.text_area(
            "Describe the problem",
            placeholder="Explain what appears incorrect on the map..."
        )

        st.subheader("Reported coordinates")

        col1, col2 = st.columns(2)

        with col1:
            reported_lat = st.number_input(
                "Reported latitude",
                min_value=-90.0,
                max_value=90.0,
                value=26.9197,
                format="%.6f"
            )

        with col2:
            reported_lon = st.number_input(
                "Reported longitude",
                min_value=-180.0,
                max_value=180.0,
                value=75.7878,
                format="%.6f"
            )

        submitted = st.form_submit_button(
            "Analyze Map Error",
            type="primary",
            use_container_width=True
        )

    # ---------------- BACKEND ANALYSIS ----------------

    if submitted:

        if not place_name.strip():
            st.error("Please enter a place name.")

        else:
            try:
                with st.spinner(
                    "Searching for the reference location and analyzing..."
                ):
                    result = analyze_map_issue(
                        place_name=place_name.strip(),
                        reported_lat=reported_lat,
                        reported_lon=reported_lon,
                        problem_type=problem_type,
                        description=description
                    )

                if not result.get("success"):
                    st.error(
                        result.get(
                            "error",
                            "Analysis could not be completed."
                        )
                    )

                else:
                    st.success("Analysis completed.")

                    st.subheader("Analysis Results")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Status",
                        result.get("status", "Unknown")
                    )

                    col2.metric(
                        "Distance from reference",
                        f'{result.get("distance_meters", 0):.1f} m'
                    )

                    col3.metric(
                        "Heuristic score",
                        f'{result.get("confidence", 0)}%'
                    )

                    st.write("**Place found:**",
                             result.get("place_name", place_name))

                    st.write(
                        "**Recommendation:**",
                        result.get(
                            "recommendation",
                            "Manual review required."
                        )
                    )

                    st.write(
                        "**Description:**",
                        result.get("description", description) or "Not provided"
                    )

                    st.warning(
                        "This score is a rule-based estimate, not a "
                        "validated probability. Verify the location "
                        "before making any real map correction."
                    )

                    # ---------------- MAP ----------------

                    st.subheader("Reported and Reference Locations")

                    reference_lat = result.get("reference_latitude")
                    reference_lon = result.get("reference_longitude")

                    map_center = [reported_lat, reported_lon]

                    if reference_lat is not None and reference_lon is not None:
                        map_center = [
                            (reported_lat + reference_lat) / 2,
                            (reported_lon + reference_lon) / 2
                        ]

                    map_view = folium.Map(
                        location=map_center,
                        zoom_start=14
                    )

                    folium.Marker(
                        [reported_lat, reported_lon],
                        popup="Reported location",
                        tooltip="Reported location",
                        icon=folium.Icon(color="red")
                    ).add_to(map_view)

                    if reference_lat is not None and reference_lon is not None:
                        folium.Marker(
                            [reference_lat, reference_lon],
                            popup="Reference location",
                            tooltip="Reference location",
                            icon=folium.Icon(color="green")
                        ).add_to(map_view)

                        folium.PolyLine(
                            [
                                [reported_lat, reported_lon],
                                [reference_lat, reference_lon]
                            ],
                            color="blue",
                            weight=3
                        ).add_to(map_view)

                    st_folium(
                        map_view,
                        use_container_width=True,
                        height=450
                    )

                    st.caption(
                        "Map reference source: "
                        + str(result.get("source", "Not specified"))
                    )

            except Exception as error:
                st.error(
                    "The backend encountered an error. "
                    "Check that agent.py, detector.py, and map_tools.py "
                    "are saved in the same project folder."
                )
                st.code(str(error))


# ---------------- ABOUT ----------------

elif page == "About":

    st.header("About MapGuard AI")

    st.write(
        "MapGuard AI is a college project prototype designed to "
        "identify possible errors in digital map locations."
    )

    st.subheader("Current features")

    st.markdown(
        """
        - Search for a reference place
        - Compare reported and reference coordinates
        - Calculate coordinate distance
        - Recommend whether a location needs review
        - Display reported and reference locations on a map
        """
    )

    st.info(
        "This prototype does not automatically modify OpenStreetMap. "
        "Human verification is required before any correction."
    )
