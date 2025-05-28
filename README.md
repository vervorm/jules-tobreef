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
5.  The backend Flask application (currently) receives the data and returns a placeholder JSON response, indicating the image was received.
6.  The frontend JavaScript updates a message area with the response from the backend. If actual segmented image data were returned, it would be displayed.

## Next Steps / Future Work

*   **Full YOLO Model Integration:**
    *   Download or train a suitable leaf segmentation model (e.g., using YOLOv8-seg from Ultralytics).
    *   Place the model weights (e.g., `best.pt`) into the `backend/models/` directory.
    *   Modify `backend/app/routes.py` in the `predict` function:
        *   Decode the base64 image string received from the frontend into an OpenCV image format.
        *   Load the YOLO model.
        *   Perform necessary preprocessing on the image to match the model's input requirements.
        *   Run inference with the YOLO model to get segmentation masks.
        *   Post-process the results: draw segmentation masks on the image, or extract mask data.
        *   Encode the processed image (with segmentation) back to a base64 string or prepare mask data to be sent to the frontend.
        *   Update the JSON response to include this `segmented_image_data`.
*   **Error Handling and UI Improvements:**
    *   Provide more specific error messages on both frontend and backend.
    *   Improve visual feedback during processing or in case of errors.
*   **Real-time Streaming (Advanced):**
    *   For a more fluid real-time experience, consider using WebSockets to stream video frames to the backend and receive segmentation results, instead of single frame captures on button click.
*   **"Further Analysis":**
    *   Once segmentation is working, implement the specific backend analysis that needs to be done on the segmented leaf (e.g., disease detection, area calculation, feature extraction).
*   **Deployment:**
    *   Containerize the application using Docker.
    *   Explore options for deploying to cloud platforms (e.g., AWS, Google Cloud, Heroku).

This README provides a guide to understanding, setting up, and running the application, as well as outlining future development paths.
