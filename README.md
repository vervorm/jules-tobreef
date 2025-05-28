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

- **`backend/`**: Contains the Flask server application.
  - **`app/`**: The main application package.
    - `__init__.py`: Initializes the Flask app, configures template and static folders to serve the frontend.
    - `routes.py`: Defines the API endpoints, including `/` to serve the main page and `/predict` to handle image processing.
  - **`models/`**: Intended to store the machine learning model files (e.g., YOLO model weights). Currently contains a `.gitkeep` file as a placeholder.
  - `run.py`: The script used to start the Flask development server.
  - `requirements.txt`: Lists the Python dependencies for the backend (Flask, OpenCV, Ultralytics).
- **`frontend/`**: Contains all the client-side files.
  - **`static/`**: Holds static assets.
    - `css/style.css`: Contains the stylesheets for the web page.
    - `js/main.js`: Handles client-side logic, including webcam access, capturing images, and sending data to the backend.
  - **`templates/index.html`**: The main HTML file for the web application.

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

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS and Linux:
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

## Docker Setup (Local Development)

### Prerequisites

- **Docker and Docker Compose:** You need to have Docker Desktop (which includes Docker Compose) installed on your system.
  - Download and install from the official Docker website: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

### Using Docker Compose (Recommended)

Docker Compose is the recommended way to run the application locally as it uses the settings defined in `docker-compose.yml`.

1.  **Build and Run:**
    Open your terminal, navigate to the project's root directory (where `docker-compose.yml` is located), and run:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image for the backend service (if it doesn't exist or if changes are detected) and then start the service.

2.  **Access the application:**
    Once the containers are running, the application will be available at:

    ```
    http://localhost:5000
    ```

3.  **Stop the application:**
    - To stop the services, press `Ctrl+C` in the terminal where `docker-compose up` is running.
    - To remove the containers (and networks created by compose), run:
      ```bash
      docker-compose down
      ```

### Using Docker (Alternative)

You can also build and run the backend service using Docker commands directly.

1.  **Build the Docker image:**
    Navigate to the project's root directory in your terminal and run:

    ```bash
    docker build -t leaf-segmentation-app ./backend
    ```

    This command builds a Docker image from the `backend/Dockerfile` and tags it as `leaf-segmentation-app`.

2.  **Run the Docker container:**
    Once the image is built, run the following command:

    ```bash
    docker run -p 5000:5000 leaf-segmentation-app
    ```

    This command starts a container from the `leaf-segmentation-app` image and maps port 5000 on your host to port 5000 in the container.

3.  **Access the application:**
    The application will be available at:
    ```
    http://localhost:5000
    ```

### Running on macOS with Colima

If you're a macOS user, Colima provides a lightweight way to run Docker containers. Here's how to set up and run this project using Colima:

1.  **Install Homebrew (if not already installed):**
    Homebrew is a package manager for macOS. If you don't have it, install it from [https://brew.sh/](https://brew.sh/).

2.  **Install Colima and Docker CLI Tools:**
    Open your Terminal and run:

    ```bash
    brew install colima docker docker-compose
    ```

    This installs Colima and the Docker command-line tools that Colima uses.

3.  **Start Colima:**
    To start Colima with default settings (typically 2 CPUs, 2GB RAM):

    ```bash
    colima start
    ```

    For better performance, especially for resource-intensive tasks like running machine learning models, consider allocating more resources:

    ```bash
    colima start --cpu 4 --memory 8 --disk 100 --vm-type=vz --mount-type=vz # For macOS Sonoma and later with vz and virtiofs
    # For older macOS versions or different preferences:
    # colima start --cpu 4 --memory 8
    ```

    Refer to Colima's documentation for the latest recommendations on VM type and mount type for best performance on your macOS version.

4.  **Verify Docker Context:**
    Colima should automatically set the Docker context. Verify this with:

    ```bash
    docker context ls
    ```

    The current context should point to `colima`. If not, you might need to run `docker context use colima`.

5.  **Clone The Project Repository:**
    If you haven't already, clone this project to your Mac and navigate into its directory:

    ```bash
    git clone <your-repository-url>
    cd <project-directory-name>
    ```

6.  **Run the Application with Docker Compose:**
    From the project's root directory (where `docker-compose.yml` is located):

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image for the backend service and start it.

7.  **Access the Application:**
    Open your web browser and navigate to `http://localhost:5000`.

8.  **Stopping the Application:**

    - In the terminal where `docker-compose up` is running, press `Ctrl+C`.
    - To remove the containers and associated networks, run: `docker-compose down`

9.  **Stopping Colima:**
    When you're done using Docker, you can stop the Colima VM to free up resources:
    ```bash
    colima stop
    ```

This setup allows you to use the Docker configurations provided in this project seamlessly on your Mac via Colima.

### Notes on Docker Development

- **Code Changes & Live Reloading:** The current Docker setup copies the application code into the image at build time. If you make code changes, you'll need to rebuild the image for them to take effect. For a more dynamic development workflow with live-reloading, you might explore uncommenting and adjusting the `volumes` section in `docker-compose.yml`. Be aware that this can sometimes introduce complexities with dependencies that are compiled or installed differently within the container versus on the host.
  - **Note on Docker Volumes Syntax:** When uncommenting `volumes` in `docker-compose.yml` for live-reloading, ensure that the `volumes:` key itself is uncommented, and that each volume entry under it is a valid list item (starting with a `- `). Improperly formatted comments or entries under an active `volumes:` key can lead to parsing errors.
- **YOLO Model Caching:** The `ultralytics` library downloads YOLO models upon their first use. These models are stored within the container. If you frequently rebuild your containers (without using Docker's build cache effectively), these models will be re-downloaded. To persist these models across container instances, you can uncomment the `yolov8_cache` named volume in `docker-compose.yml`. You may need to verify the exact cache path used by `ultralytics` inside the container (e.g., `/root/.cache/ultralytics` or similar) and adjust the volume mapping if necessary.

## How it Works (Briefly)

1.  The frontend (`index.html` and `main.js`) accesses the user's webcam and displays the video feed.
2.  The user clicks the "Capture & Segment" button.
3.  The current frame from the video is captured on a canvas and converted to a base64 encoded PNG image.
4.  This image data is sent to the backend `/predict` endpoint via a POST request.
5.  The backend Flask application (`backend/app/routes.py`) processes the image using a YOLOv8-seg model (`yolov8n-seg.pt` by default) to perform instance segmentation.
6.  The backend calculates the percentage of the total image area covered by the largest segmented object.
7.  The backend returns a JSON response containing:
    - The processed image (with segmentation masks drawn) as a base64 data URL.
    - The calculated area percentage.
    - A boolean flag indicating if this area percentage exceeds a threshold (currently 50%).
8.  The frontend JavaScript (`frontend/static/js/main.js`) updates the UI:
    - Displays the segmented image.
    - Shows the area percentage.
    - If the area threshold is exceeded, a button "Upload Cropped Leaf for Further Analysis" is displayed.
    - Clicking this button currently calls a placeholder backend endpoint (`/upload_cropped_leaf`).

## Features

- Webcam integration for live video feed.
- Image capture from video stream.
- Leaf segmentation using YOLOv8-seg model.
- Calculation of the largest segmented object's area percentage.
- Conditional display of a button for further analysis based on the area percentage.
- Basic frontend and backend structure for further development.

## Setup and Installation

(This section remains largely unchanged, ensure `backend/requirements.txt` includes `ultralytics` and `opencv-python-headless`)

...

## Backend Details

- The core segmentation logic is in `backend/app/routes.py` within the `/predict` endpoint. This includes image decoding, YOLOv8 model inference, mask plotting, and area calculation.
- A new placeholder endpoint `/upload_cropped_leaf` has been added to `backend/app/routes.py` to demonstrate future functionality.

### Server-Side Image Saving

- **Functionality:** Each time a successful prediction is made, the backend automatically saves the processed image (the one with segmentation masks drawn on it) to the server.
- **Save Location:** Images are saved in the `backend/saved_segmented_images/` directory. When running inside a Docker container, this path corresponds to `/app/saved_segmented_images/`.
- **Filename Convention:** Images are saved with filenames like `segmented_YYYYMMDD_HHMMSS_ffffff.png`, ensuring uniqueness based on the timestamp of processing.
- **Docker Persistence for Saved Images:** When running the application with Docker, the `saved_segmented_images/` directory resides within the container. If you stop and remove the container, these saved images will be deleted. To persist these images across container restarts, you can mount a Docker volume or a host directory to `/app/saved_segmented_images/` in your `docker-compose.yml`. For example:

  ```yaml
  services:
    backend:
      # ... other configurations ...
      volumes:
        # Example: Mount a host directory to the container path
        - ./my_saved_images_on_host:/app/saved_segmented_images
        # Or using a named volume (ensure 'saved_images_volume' is defined at the top level):
        # - saved_images_volume:/app/saved_segmented_images
  # If using a named volume, define it at the top level of docker-compose.yml:
  # volumes:
  #   saved_images_volume:
  ```

  Replace `./my_saved_images_on_host` with the actual path on your host machine where you want to store the images.

## Frontend Details

- `frontend/templates/index.html` has been updated to include elements for displaying the area percentage and the conditional "Upload Cropped Leaf" button.
- `frontend/static/js/main.js` now handles the updated backend response, displays the new information, manages the visibility of the conditional button, and calls the `/upload_cropped_leaf` placeholder endpoint.

## Next Steps / Future Work

- **Refine "Upload Cropped Leaf" Functionality:**
  - **Frontend:** Implement actual image cropping. This could involve:
    - Using mask coordinates (if the YOLO model provides them in a usable format for precise cropping).
    - Allowing the user to draw a bounding box or adjust a pre-defined crop area on the segmented image.
  - **Backend:** Fully implement the `/upload_cropped_leaf` endpoint to:
    - Receive the cropped image data.
    - Store the image (e.g., in a file system or database).
    - Perform further analysis on the cropped leaf (e.g., disease detection, more detailed feature extraction).
- **YOLO Model Selection & Improvement:**
  - The initial request mentioned "YOLOv11". As a specific "YOLOv11" model for segmentation wasn't readily available or standard at the time of implementation, a suitable and widely-used YOLO segmentation model, YOLOv8-seg (`yolov8n-seg.pt`), was chosen. If a specific "YOLOv11" model becomes available and is preferred, it can be integrated.
  - Improve segmentation accuracy by:
    - Using larger pre-trained YOLOv8-seg models (e.g., `yolov8s-seg.pt`, `yolov8m-seg.pt`). This may require more processing power.
    - Training a custom YOLOv8-seg model on a specific dataset of leaves for better performance on the target task.
- **Error Handling and UI Improvements:**
  - Provide more specific error messages on both frontend and backend.
  - Improve visual feedback during processing or in case of errors (e.g., loading indicators).
- **Real-time Streaming (Advanced):**
  - For a more fluid real-time experience, consider using WebSockets to stream video frames to the backend and receive segmentation results, instead of single frame captures on button click. This would be a more significant architectural change.
- **Deployment:**
  - Containerize the application using Docker.
  - Explore options for deploying to cloud platforms (e.g., AWS, Google Cloud, Heroku).

This README provides a guide to understanding, setting up, and running the application, as well as outlining future development paths.

├── IMAGES/
│ └── healthy-infected/
│ ├── healthy
│ └── infected
└── SEGMENTED/
└── healthy-infected/
├── healthy
└── infected
