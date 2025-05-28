from flask import Blueprint, request, jsonify, render_template
from ultralytics import YOLO
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os
from datetime import datetime

bp = Blueprint('main', __name__)

# Load the YOLOv8 model (consider loading once globally if performance becomes an issue)
# For this subtask, loading it here is fine. Using a small model for speed.
# The model will be downloaded automatically by ultralytics if not found.
try:
    model = YOLO('yolov8n-seg.pt') 
except Exception as e:
    # If model loading fails, the app might not be usable.
    # Log this prominently or handle as a critical error.
    print(f"CRITICAL: Failed to load YOLO model: {e}")
    model = None 

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'message': 'Error: YOLO Model not loaded.', 'error': 'Server configuration issue'}), 500
        
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'message': 'Error: No image data received.', 'error': 'Bad request'}), 400
        
        image_data_b64_prefixed = data['image']
        
        # Decode base64 image
        # Expecting data URL like "data:image/png;base64,actual_base64_string"
        if ',' not in image_data_b64_prefixed:
            return jsonify({'message': 'Error: Invalid image data format.', 'error': 'Bad request'}), 400
            
        image_data_b64 = image_data_b64_prefixed.split(',')[1]
        img_bytes = base64.b64decode(image_data_b64)
        img_pil = Image.open(BytesIO(img_bytes))
        
        # Convert PIL Image to OpenCV format (BGR)
        image_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        if image_cv is None:
             return jsonify({'message': 'Error: Could not decode image.', 'error': 'Image processing failed'}), 400


        # Perform YOLOv8 inference
        results = model.predict(image_cv, verbose=False, conf=0.5) # Added conf for potentially cleaner output

        annotated_image_cv = image_cv.copy() # Default to original if no masks
        area_percentage = 0.0
        largest_mask_area = 0.0
        
        # Initialize annotated_image_cv based on whether masks are present
        if results and results[0].masks is not None and len(results[0].masks.data) > 0:
            annotated_image_cv = results[0].plot() # This plots masks, boxes, labels
        else:
            # If no masks, annotated_image_cv remains a copy of the original image_cv
            # Or, if you want to ensure it's always the plotted image (even if empty of detections):
            annotated_image_cv = results[0].plot() # this will return the original image if no detections/masks

        # --- Add image saving logic here ---
        save_dir = 'saved_segmented_images' # This will be /app/saved_segmented_images in Docker
        os.makedirs(save_dir, exist_ok=True) # Create directory if it doesn't exist

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f") # Use datetime for unique names
        filename = f"segmented_{timestamp}.png"
        save_path = os.path.join(save_dir, filename)

        try:
            if annotated_image_cv is not None and annotated_image_cv.size > 0 : # Check if image is valid
                cv2.imwrite(save_path, annotated_image_cv)
                print(f"INFO: Saved segmented image to {save_path}") # Add a log/print
            else:
                print(f"WARNING: Annotated image is empty or invalid. Not saving.")
        except Exception as e:
            print(f"ERROR: Could not save image to {save_path}: {e}")
        # --- End of image saving logic ---

        if results and results[0].masks is not None and len(results[0].masks.data) > 0:
            image_total_area = image_cv.shape[0] * image_cv.shape[1]
            
            for mask_polygon_xy in results[0].masks.xy:
                current_area = cv2.contourArea(np.array(mask_polygon_xy).astype(np.int32))
                if current_area > largest_mask_area:
                    largest_mask_area = current_area
            
            if image_total_area > 0:
                area_percentage = (largest_mask_area / image_total_area) * 100
            else:
                area_percentage = 0 
        else:
            # No masks detected, keep original image and 0 percentage
            pass

        # Encode the processed image (with or without masks) back to base64
        _, buffer = cv2.imencode('.png', annotated_image_cv)
        processed_image_b64 = base64.b64encode(buffer).decode('utf-8')
        processed_image_data_url = f"data:image/png;base64,{processed_image_b64}"
        
        area_exceeds_threshold = area_percentage > 50

        return jsonify({
            'message': 'Processing complete.' if results and results[0].masks else 'Processing complete, no objects segmented.',
            'segmented_image_data': processed_image_data_url,
            'area_percentage': round(area_percentage, 2),
            'area_exceeds_threshold': area_exceeds_threshold
        })

    except Exception as e:
        print(f"Error in /predict: {e}") # Log error to backend console
        # Consider more specific error logging if possible (e.g., stack trace)
        return jsonify({'message': 'Error processing request on backend.', 'error': str(e)}), 500

@bp.route('/upload_cropped_leaf', methods=['POST'])
def upload_cropped_leaf():
    try:
        # data = request.get_json() # You might want to get data in the future
        # For now, just a placeholder
        # For example, log that it was called:
        # current_app.logger.info("Placeholder /upload_cropped_leaf called.")
        print("Placeholder /upload_cropped_leaf called.") # Using print for now
        return jsonify({'message': 'Placeholder for cropped leaf upload received.'}), 200
    except Exception as e:
        # current_app.logger.error(f"Error in /upload_cropped_leaf: {e}")
        print(f"Error in /upload_cropped_leaf: {e}") # Using print for now
        return jsonify({'message': 'Error processing placeholder request.', 'error': str(e)}), 500
