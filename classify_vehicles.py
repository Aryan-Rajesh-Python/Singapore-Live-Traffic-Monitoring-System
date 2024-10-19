# classify_vehicles.py
import torch

# Load YOLOv5 model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Function to classify vehicles in an image
def classify_vehicles(image_path):
    # Perform inference using YOLOv5 model
    results = model(image_path)

    # Get detections in pandas dataframe
    detections = results.pandas().xyxy[0]

    # Print out detections for debugging
    print("Detections:", detections)  # Debugging line
    print("Detected Classes:", detections['name'].unique())  # Debugging line

    # Filter vehicle classes (car, bus, truck, etc.)
    vehicle_classes = ['car', 'bus', 'truck', 'motorbike', 'bicycle']
    vehicles_detected = detections[detections['name'].isin(vehicle_classes)]

    # Count each vehicle type
    vehicle_counts = vehicles_detected['name'].value_counts()

    # Print vehicle counts for debugging
    print("Vehicle Counts:", vehicle_counts)  # Debugging line
    return vehicle_counts
