const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('captureBtn');
const segmentedImage = document.getElementById('segmentedImage');
const messageArea = document.getElementById('messageArea');
const context = canvas.getContext('2d');
const areaPercentageDisplay = document.getElementById('areaPercentage'); // Added
const uploadCroppedBtn = document.getElementById('uploadCroppedBtn'); // Added

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
        
        messageArea.textContent = result.message || 'Processing complete.';

        if (result.segmented_image_data) {
            segmentedImage.src = result.segmented_image_data;
            segmentedImage.style.display = 'block';
        } else {
            segmentedImage.style.display = 'none';
            messageArea.textContent = 'Error: No segmented image data received.';
        }

        if (result.area_percentage !== undefined) {
            areaPercentageDisplay.textContent = `Largest object covers: ${result.area_percentage.toFixed(2)}% of image.`;
        } else {
            areaPercentageDisplay.textContent = '';
        }

        if (result.area_exceeds_threshold) {
            uploadCroppedBtn.style.display = 'block';
        } else {
            uploadCroppedBtn.style.display = 'none';
        }

    } catch (error) {
        console.error('Error sending image to backend:', error);
        messageArea.textContent = `Error processing image: ${error.message}`;
        segmentedImage.style.display = 'none';
        areaPercentageDisplay.textContent = '';
        uploadCroppedBtn.style.display = 'none';
    }
});

// Add event listener for the new button
uploadCroppedBtn.addEventListener('click', async () => {
   messageArea.textContent = 'Upload Cropped Leaf button clicked. Calling placeholder endpoint...';
   try {
       const response = await fetch('/upload_cropped_leaf', { 
           method: 'POST',
           headers: { // Optional: If your placeholder endpoint expects JSON
            'Content-Type': 'application/json',
           },
            // body: JSON.stringify({ key: 'value' }) // Optional: if you want to send data
        });
       const data = await response.json();
       messageArea.textContent = 'Upload Cropped Leaf: ' + data.message;
   } catch (err) {
       messageArea.textContent += ' Error calling placeholder endpoint for upload.';
       console.error('Error calling /upload_cropped_leaf:', err);
   }
});

initCamera();
