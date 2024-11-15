# importing the cv2 library
import cv2
from PIL import Image
class face_capture() :
    def __init__(self,target_file_name):
        #Opens Camera
        video = cv2.VideoCapture(0)
        # loading the haar case algorithm file into alg variable
        alg = "xml/haarcascade_frontalface_default.xml"
        # passing the algorithm to OpenCV
        haar_cascade = cv2.CascadeClassifier(alg)
        # Reads frames from camera
        ret, frame = video.read()
        # detecting the faces
        faces = haar_cascade.detectMultiScale(
            frame, scaleFactor=1.05, minNeighbors=2
        )

        i = 0
        # for each face detected
        for x, y, w, h in faces:
            # crop the image to select only the face
            cropped_image = frame[y : y + h, x : x + w]
            cv2.imwrite(
                ('stored-faces/'+target_file_name+'.jpg'),
                cropped_image,
            )
            i = i + 1
        video.release()
        self.image = Image.open('stored-faces/'+target_file_name+'.jpg')
        self.filename = target_file_name


class face_video() :
    def __init__(self):
        #Opens Camera
        video = cv2.VideoCapture(0)
        # loading the haar case algorithm file into alg variable
        face_classifier = cv2.CascadeClassifier("../face-detection-db/xml/haarcascade_frontalface_default.xml")
        while True:
            ret, frame = video.read()
            faces = face_classifier.detectMultiScale(frame,1.1,12)
            for (x, y, width, height) in faces:
                x2, y2 = x+ width, y+ height
                cropped_image = frame[y : y + height, x : x + width]
                self.frame = Image.fromarray(cropped_image)
                cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 3)
                self.coord = [(x,y),(x2,y2),(255,0,0)]
            cv2.imshow('Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()