import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'images'
images = []
classNames = []
myList = os.listdir(path)

# print(myList)

for cls in myList:
    current_image = cv2.imread(f'{path}/{cls}')
    images.append(current_image)
    # Remove the extensions
    classNames.append(os.path.splitext(cls)[0])
print(classNames)


def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode_img = face_recognition.face_encodings(img)[0]
        encode_list.append(encode_img)
    return encode_list


def mark_attendance(name):
    with open('Attendance_Sheet.csv', 'r+') as file:
        attendance_list = file.readlines()
        name_list = []
        # print(attendance_list)
        for line in attendance_list:
            entry = line.split(',')
            # entry 0 is the Name and we're appending only names and the
            # time will be coming from the system
            name_list.append(entry[0])
        if name not in name_list:
            tic = datetime.now()
            date_string = tic.strftime('%H:%M:%S')
            file.writelines(f'\n{name}, {date_string}')


# mark_attendance('Imran')

encode_list_known_faces = find_encodings(images)
# print(len(encode_list_known_faces))
print("Encoding Completes")

webcam = cv2.VideoCapture(0)
while True:
    is_successful, frame = webcam.read()
    frame_resize = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    frame_resize = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGB)

    faces_in_frame = face_recognition.face_locations(frame_resize)  # the locations of faces
    encode_frame = face_recognition.face_encodings(frame_resize, faces_in_frame)

    for encode_face, face_loc in zip(encode_frame, faces_in_frame):
        comparison = face_recognition.compare_faces(encode_list_known_faces, encode_face)
        face_distance = face_recognition.face_distance(encode_list_known_faces, encode_face)
        # print(face_distance)
        comparison_index = np.argmin(face_distance)

        if comparison[comparison_index]:
            name = classNames[comparison_index].upper()
            # print(name)
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (252, 255, 255), 2)
            mark_attendance(name)

    cv2.imshow('Webcam', frame)
    cv2.waitKey(1)
