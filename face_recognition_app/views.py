# from django.shortcuts import render
# import cv2
# import numpy as np
# from django.http import JsonResponse
# # Create your views here.



# def detect_faces(request):
#     # Get the video frame sent from the client
#     video_frame = np.frombuffer(request.body, dtype=np.uint8)
#     video_frame = cv2.imdecode(video_frame, cv2.IMREAD_COLOR)

#     # Perform face detection using OpenCV
#     face_cascade = cv2.CascadeClassifier('D:/coding/projects/face-recognition(with WebRTC and Django)/env/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
#     gray_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

#     # Convert the faces to JSON response
#     faces_json = []
#     for (x, y, w, h) in faces:
#         faces_json.append({
#             'x': x,
#             'y': y,
#             'width': w,
#             'height': h,
#         })

#     return JsonResponse({'faces': faces_json})



# def home(request):
#     return render(request, 'home.html')


# face_recognition_app/views.py

# face_recognition_app/views.py

import cv2
import numpy as np
import base64
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer
from .models import UserProfile


def detect_faces(request):
    print(request.body)  # Add this line to inspect the value of request.body

    # Get the video frame sent from the client
    data = json.loads(request.body)
    frame_data = base64.b64decode(data['frame_data'])

    # Convert the frame data to a NumPy array
    nparr = np.frombuffer(frame_data, np.uint8)

    # Decode the image array
    video_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform face detection using OpenCV
    face_cascade = cv2.CascadeClassifier('D:/coding/projects/face-recognition(with WebRTC and Django)/env/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    # Convert the faces to JSON response
    faces_json = []
    for (x, y, w, h) in faces:
        faces_json.append({
            'x': x,
            'y': y,
            'width': w,
            'height': h,
        })

    return JsonResponse({'faces': faces_json})


class UserProfileAPIView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)