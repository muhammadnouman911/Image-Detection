import torch
from pathlib import Path
import cv2
from matplotlib import pyplot as plt

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/yolov5_custom3/weights/best.pt')

# Set model to evaluation mode
model.eval()

# Define the function to perform inference
def detect(image_path):
    # Read image
    img = cv2.imread(image_path)
    
    # Check if image was loaded successfully
    if img is None:
        print(f"Error: Could not load image {image_path}")
        return

    # Run inference
    results = model(img)

    # Render results (bounding boxes and labels on image)
    results.render()

    # Convert from BGR to RGB for display
    img_with_boxes = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Display the image
    plt.imshow(img_with_boxes)
    plt.axis('off')  # Hide axis
    plt.show()

    # Save the image with boxes
    output_path = Path(image_path).stem + '_result.jpg'
    cv2.imwrite(output_path, img)

# Path to your image
image_path = 'both.jpg'  # Replace with your actual image path

# Perform detection
detect(image_path)
