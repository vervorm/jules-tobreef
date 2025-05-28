const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('captureBtn');
const segmentedImage = document.getElementById('segmentedImage');
const messageArea = document.getElementById('messageArea');
const context = canvas.getContext('2d');

// Access webcam
async function initCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing webcam: ", err);
        messageArea.textContent = "Error accessing webcam. Please ensure permissions are granted.";
    }
}

captureBtn.addEventListener('click', async () => {
    messageArea.textContent = 'Capturing and processing...';
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataURL = canvas.toDataURL('image/png');

    try {
        const response = await fetch('/predict', { // Assuming Flask serves frontend and backend on same origin
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageDataURL }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.segmented_image_data && result.segmented_image_data !== 'dummy_segmented_data') {
            // Assuming backend returns base64 image data for the segmented image
            segmentedImage.src = result.segmented_image_data; 
            segmentedImage.style.display = 'block';
            messageArea.textContent = result.message || 'Processing complete.';
        } else if (result.segmented_image_data === 'dummy_segmented_data') {
             messageArea.textContent = result.message || 'Received dummy data from backend.';
             segmentedImage.style.display = 'none';
        } else {
            messageArea.textContent = 'Error: No segmented image data received.';
            segmentedImage.style.display = 'none';
        }

    } catch (error) {
        console.error('Error sending image to backend:', error);
        messageArea.textContent = `Error processing image: ${error.message}`;
        segmentedImage.style.display = 'none';
    }
});

initCamera();
