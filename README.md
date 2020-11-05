# AI-Face-Recognition-Attendance-System
An attendance system based on facial recognition where it'll mark the person's attendance by recognizing his/her face. 
By seeing via the webcam the model can recognize the faces you provide in the ```images``` folder. In the ```images``` 
put the images of the person which I called the known faces and so you be get to go. 

## The Code Flow
-	First read the path and get all the images' names to a list from the ```images``` folder
-	Then remove the extension from the images
-	The method ```find_encodings()``` do finds all the encodings of the faces' images in the list
-	The method ```mark_attendance()``` do opens the ```Attendance_Sheet.csv``` file and write the name of the person recognized by it also in the next column, 
means this method do mark the attendace of the person 
it do writes the time, i-e the current time with the help of ```tic = datetime.now()```
-	Then until the webcam stream is open capture the frames
-	First resize the frame size and reduce it by 25%
-	Find the face locations of all the faces in the frames
-	Find all the endcodings of the faces in the frames
-	Now in all the locations and encodings do compare it to the encodings of those which are in the ```images``` folder
-	If both are same, draw the retangle around that and put the name of that person below the face
-	At last if the person is recognized do mark his/her attendance