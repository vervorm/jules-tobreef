# Real-time Leaf Segmentation Web App

## Overview
This project is a web application designed for real-time leaf segmentation. Users can capture images from their webcam, and the application will process the image to segment the leaf. Currently, the backend returns a placeholder response, but it's designed for integration with a YOLO (You Only Look Once) model for actual segmentation.

## Project Structure
The project is divided into a `frontend` and a `backend` directory.

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py  # Flask app initialization, frontend serving config
│   │   └── routes.py    # API routes (/ and /predict)
│   ├── models/          # (Placeholder for YOLO model files, e.g., .pt)
│   │   └── .gitkeep     # Ensures the directory is tracked
│   ├── run.py           # Script to run the Flask backend
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css  # Basic styling
│   │   └── js/
│   │       └── main.js    # Frontend logic (camera, API calls)
│   └── templates/
│       └── index.html   # Main HTML page
└── README.md            # This file
```

*   **`backend/`**: Contains the Flask server application.
    *   **`app/`**: The main application package.
        *   `__init__.py`: Initializes the Flask app, configures template and static folders to serve the frontend.
        *   `routes.py`: Defines the API endpoints, including `/` to serve the main page and `/predict` to handle image processing.
    *   **`models/`**: Intended to store the machine learning model files (e.g., YOLO model weights). Currently contains a `.gitkeep` file as a placeholder.
    *   `run.py`: The script used to start the Flask development server.
    *   `requirements.txt`: Lists the Python dependencies for the backend (Flask, OpenCV, Ultralytics).
*   **`frontend/`**: Contains all the client-side files.
    *   **`static/`**: Holds static assets.
        *   `css/style.css`: Contains the stylesheets for the web page.
        *   `js/main.js`: Handles client-side logic, including webcam access, capturing images, and sending data to the backend.
    *   **`templates/index.html`**: The main HTML file for the web application.

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Python dependencies:**
    Navigate to the `backend` directory if you are not already there and install the required packages:
    ```bash
    pip install -r backend/requirements.txt
    ```

## Running the Application

1.  **Run the backend Flask server:**
    Ensure your virtual environment is activated. From the root directory of the project, run:
    ```bash
    python backend/run.py
    ```
    You should see output indicating the server is running, typically on `http://127.0.0.1:5000/`.

2.  **Access the web application:**
    Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

## How it Works (Briefly)

1.  The frontend (`index.html` and `main.js`) accesses the user's webcam and displays the video feed.
2.  The user clicks the "Capture & Segment" button.
3.  The current frame from the video is captured on a canvas and converted to a base64 encoded PNG image.
4.  This image data is sent to the backend `/predict` endpoint via a POST request.
5.  The backend Flask application (`backend/app/routes.py`) processes the image using a YOLOv8-seg model (`yolov8n-seg.pt` by default) to perform instance segmentation.
6.  The backend calculates the percentage of the total image area covered by the largest segmented object.
7.  The backend returns a JSON response containing:
    *   The processed image (with segmentation masks drawn) as a base64 data URL.
    *   The calculated area percentage.
    *   A boolean flag indicating if this area percentage exceeds a threshold (currently 50%).
8.  The frontend JavaScript (`frontend/static/js/main.js`) updates the UI:
    *   Displays the segmented image.
    *   Shows the area percentage.
    *   If the area threshold is exceeded, a button "Upload Cropped Leaf for Further Analysis" is displayed.
    *   Clicking this button currently calls a placeholder backend endpoint (`/upload_cropped_leaf`).

## Features

*   Webcam integration for live video feed.
*   Image capture from video stream.
*   Leaf segmentation using YOLOv8-seg model.
*   Calculation of the largest segmented object's area percentage.
*   Conditional display of a button for further analysis based on the area percentage.
*   Basic frontend and backend structure for further development.

## Setup and Installation
(This section remains largely unchanged, ensure `backend/requirements.txt` includes `ultralytics` and `opencv-python-headless`)

...

## Backend Details
*   The core segmentation logic is in `backend/app/routes.py` within the `/predict` endpoint. This includes image decoding, YOLOv8 model inference, mask plotting, and area calculation.
*   A new placeholder endpoint `/upload_cropped_leaf` has been added to `backend/app/routes.py` to demonstrate future functionality.

## Frontend Details
*   `frontend/templates/index.html` has been updated to include elements for displaying the area percentage and the conditional "Upload Cropped Leaf" button.
*   `frontend/static/js/main.js` now handles the updated backend response, displays the new information, manages the visibility of the conditional button, and calls the `/upload_cropped_leaf` placeholder endpoint.

## Next Steps / Future Work

*   **Refine "Upload Cropped Leaf" Functionality:**
    *   **Frontend:** Implement actual image cropping. This could involve:
        *   Using mask coordinates (if the YOLO model provides them in a usable format for precise cropping).
        *   Allowing the user to draw a bounding box or adjust a pre-defined crop area on the segmented image.
    *   **Backend:** Fully implement the `/upload_cropped_leaf` endpoint to:
        *   Receive the cropped image data.
        *   Store the image (e.g., in a file system or database).
        *   Perform further analysis on the cropped leaf (e.g., disease detection, more detailed feature extraction).
*   **YOLO Model Selection & Improvement:**
    *   The initial request mentioned "YOLOv11". As a specific "YOLOv11" model for segmentation wasn't readily available or standard at the time of implementation, a suitable and widely-used YOLO segmentation model, YOLOv8-seg (`yolov8n-seg.pt`), was chosen. If a specific "YOLOv11" model becomes available and is preferred, it can be integrated.
    *   Improve segmentation accuracy by:
        *   Using larger pre-trained YOLOv8-seg models (e.g., `yolov8s-seg.pt`, `yolov8m-seg.pt`). This may require more processing power.
        *   Training a custom YOLOv8-seg model on a specific dataset of leaves for better performance on the target task.
*   **Error Handling and UI Improvements:**
    *   Provide more specific error messages on both frontend and backend.
    *   Improve visual feedback during processing or in case of errors (e.g., loading indicators).
*   **Real-time Streaming (Advanced):**
    *   For a more fluid real-time experience, consider using WebSockets to stream video frames to the backend and receive segmentation results, instead of single frame captures on button click. This would be a more significant architectural change.
*   **Deployment:**
    *   Containerize the application using Docker.
    *   Explore options for deploying to cloud platforms (e.g., AWS, Google Cloud, Heroku).

This README provides a guide to understanding, setting up, and running the application, as well as outlining future development paths.
