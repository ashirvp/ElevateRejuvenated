import cv2
from app.model import FacialExpressionModel
import numpy as np
from app.models import Patient
facec = cv2.CascadeClassifier('app/haarcascade_frontalface_default.xml')
model = FacialExpressionModel("app/model.json", "app/model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
import pandas as pd
import pickle
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        a=pickle.load(open('app/emotions.pkl','rb'))
        _, fr = self.video.read()
        print(type(fr))
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
            a.append(pred)
            pickle.dump(a,open('app/emotions.pkl','wb'))
        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()