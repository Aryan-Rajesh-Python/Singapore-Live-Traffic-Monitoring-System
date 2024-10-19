import time
import streamlit as st
from fetch_images import fetch_traffic_images, download_image
from classify_vehicles import classify_vehicles

# Dictionary of locations and their respective image URLs
locations = {
    "Woodlands Checkpoint": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html#trafficCameras",
    "Tuas Checkpoint": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/tuas.html#trafficCameras",
    "KJE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/kje.html#trafficCameras",
    "SLE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/sle.html#trafficCameras",
    "TPE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/tpe.html#trafficCameras",
    "BKE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/bke.html#trafficCameras",
    "PIE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/pie.html#trafficCameras",
    "KPE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/kpe.html#trafficCameras",
    "CTE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/cte.html#trafficCameras",
    "AYE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/aye.html#trafficCameras",
    "ECP": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/ecp.html#trafficCameras",
    "MCE": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/mce.html#trafficCameras",
    "Loyang Ave/Tanah Merah Coast Road": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/ltm.html#trafficCameras",
    "Sentosa Gateway": "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/stg.html#trafficCameras",
}

def traffic_monitor_dashboard(interval=30, duration=1800):
    st.title("Real-Time Singapore Traffic Monitoring System")

    # Dropdown for selecting a location
    selected_location = st.selectbox("Select Location", list(locations.keys()))

    start_time = time.time()

    while time.time() - start_time < duration:
        # Fetch all traffic image URLs based on the selected location
        image_urls = fetch_traffic_images(locations[selected_location])

        if not image_urls:
            st.error("No traffic images found. Please check the URL or try again later.")
            break  # Exit the loop if no images are found

        # Initialize a total vehicle counts dictionary
        vehicle_counts_total = {}

        for image_url in image_urls:
            image_path = download_image(image_url)

            # Classify vehicles
            vehicle_counts = classify_vehicles(image_path)

            # Combine counts manually
            for vehicle, count in vehicle_counts.items():
                if vehicle in vehicle_counts_total:
                    vehicle_counts_total[vehicle] += count
                else:
                    vehicle_counts_total[vehicle] = count

            # Display the latest image
            st.image(image_path, caption=f"Traffic Image from {selected_location}", use_column_width=True)
            st.write("Vehicle Counts for this image:")
            st.write(vehicle_counts)

        # Display total vehicle counts
        st.write("Total Vehicle Counts:")
        st.write(vehicle_counts_total)

        # Refresh every interval (e.g., 30 seconds)
        time.sleep(interval)
        st.experimental_rerun()

# Run the dashboard for 30 minutes with a 30-second interval
if __name__ == "__main__":
    traffic_monitor_dashboard(interval=30, duration=1800)