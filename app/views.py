from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
import cv2
import base64
import numpy as np
from django.shortcuts import render
import json
from django.http import HttpResponse
import face_recognition
import cvzone
import os
import pickle
from .models import Profile
# Create your views here.


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('token')
        else:
            messages.info(request, 'Incorrect credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        patientID = request.POST['patientID']
        age = request.POST['age']
        aadhaar = request.POST['aadhaar']
        gender = request.POST['gender']
        address = request.POST['address']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            profile = Profile.objects.create(user=user, firstname=firstname, lastname=lastname, patientID=patientID, age=age, aadhaar=aadhaar, gender=gender, address=address)
            profile.save()
            return redirect('login')
    else:
        return render(request, 'register.html')

def token(request):
    return render(request, 'webcam.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def webcam(request):
    return render(request,'webcam.html')

ind = 0
# @csrf_exempt
def process_frame(request):
    # try:
    print("Loading Encode File ...")
    file = open("C:\\Users\\ACER\\Desktop\\test\\TEST\myApp\\Stuff\\EncodeFile.p", 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode File Loaded")

    # print(request.method)
    if request.method == "POST":
        frame = json.loads(request.body)
        for key, value in frame.items():
            frame_data = value
        # print(frame_data)
        frame_data = frame_data.split(",")[1]
        frame_bytes = base64.b64decode(frame_data)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print("matches", matches) # [True, False]
                # print("faceDis", faceDis)

                matchIndex = np.argmin(faceDis)
                # print("Match Index", matchIndex)

                if matches[matchIndex]:
                    print("Known Face Detected")
                    global ind
                    ind = studentIds[matchIndex]
                    print(ind) # => 15243
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = x1, y1, x2 - x1, y2 - y1
                    # frame = cvzone.cornerRect(frame, bbox, rt=0, colorC=(0, 255, 255))

    # cv2.imshow("Image", img)
    context = {
        'index' : ind,
        'Match' : True,
    }
    # return render(request, 'process_frame.html', context)
    return redirect('process_frame', {"context" : context})

    # except Exception as e:
    #     print("Error processing frame:", e)
    #     return HttpResponse("Error processing frame: " + str(e), status=500)

        # imgOutput = cv2.imencode('.jpg', img)[1].tobytes()
        # yield (b'--frame\r\n'
        #         b'Content-Type: image/jpeg\r\n\r\n' + imgOutput + b'\r\n')

# f'<h1> Known Face Detected <br> Matched Index: ${ind}</h1>'
# Taken from Images directory
folderPath = 'C:\\Users\\ACER\\Desktop\\Healthista\\Healthista-main\\app\\Stuff\\Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    # fileName = f'{folderPath}/{path}'
    # bucket = storage.bucket()
    # blob = bucket.blob(fileName)
    # blob.upload_from_filename(fileName)


    print(path)
    print(os.path.splitext(path)[0])
print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

# def my_view(request):
#     my_models = Profile.objects.all()
#     return render(request, 'process_frame.html', {'my_models': my_models})