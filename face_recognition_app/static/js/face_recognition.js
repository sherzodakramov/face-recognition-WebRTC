// # face_recognition.js

// # Get video element
// const videoElement = document.getElementById('video-element');

// # Request user media access
// navigator.mediaDevices.getUserMedia({ video: true })
//   .then((stream) => {
//     // Set the video source to the user's webcam
//     videoElement.srcObject = stream;
//   })
//   .catch((error) => {
//     console.error('Error accessing webcam:', error);
//   });


// face_recognition.js

// Get video element
const videoElement = document.getElementById('video-element');
  
// Get results list element
const resultsListElement = document.getElementById('results-list');
  
// Request user media access
navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => {
    // Set the video source to the user's webcam
    videoElement.srcObject = stream;

    // Send video frames to the server for processing
    const sendVideoFrames = () => {
      // Capture a frame from the video
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
      const frameData = canvas.toDataURL('image/jpeg');

      // Send the frame data to the server using AJAX
      const xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // Update the UI with the recognition results
            const response = JSON.parse(xhr.responseText);
            updateResultsUI(response.faces);
          } else {
            console.error('Error processing video frame:', xhr.status);
          }
        }
      };
      xhr.open('POST', '/detect_faces');
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify({ frame_data: frameData }));
  
      // Schedule the next frame to be sent
      requestAnimationFrame(sendVideoFrames);
    };
  
    // Start sending video frames
    sendVideoFrames();
 })
  .catch((error) => {
    console.error('Error accessing webcam:', error);
  });
  
// Update the UI with the recognition results
function updateResultsUI(faces) {
  // Clear the results list
  resultsListElement.innerHTML = '';

  // Add each face to the results list
  faces.forEach((face) => {
    const listItem = document.createElement('li');
    listItem.textContent = `Face detected at (${face.x}, ${face.y}) with width ${face.width} and height ${face.height}`;
    resultsListElement.appendChild(listItem);
  });
}