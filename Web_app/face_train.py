import numpy as np
import cv2 
import pickle 
import os
import face_recognition
from flask_mysqldb import MySQL
from datetime import datetime
import mysql.connector
from flask import request,render_template





db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="web_app"
)

from datetime import datetime

#now = datetime.now()
#time_str = now.strftime("%I:%M %p")
#print(time_str)
import datetime

timestamp = "2023-04-21 15:04:34"
datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
formatted_time = datetime_obj.strftime('%I:%M %p')
print(formatted_time)


"""
folderModePath= 'student_image'
if not os.path.isdir('student_image'):
    os.makedirs('student_image')

def findTrain(imglist):
    encodeList = []
    for img in imglist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #resize = cv2.resize(img,(0,0), None , 0.25,0.25)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList    


# ---------------- WRITING THE IMAGE FILE IN EncoderFile.p -------------------- #





cursor = db.cursor()

sql = "INSERT INTO student_main (full_name,course,year_level,gender,face_trained) VALUES (%s,%s,%s,%s,%s)"
values = ("Irene","BSIT","4th year","male",pickle.dumps(encodeListKnownwithIds))
cursor.execute(sql,values)
db.commit()
cursor.close()

print("FIle successfully Save in Database")

"""