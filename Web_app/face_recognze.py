from functools import wraps
import numpy as np
import cv2
import pickle 
import face_recognition
from Web_app import app,bycryt
from flask_mail import Message,Mail
from Web_app.model import Model
from datetime import date,datetime,timedelta
from flask import render_template,redirect,url_for,flash,session,request,make_response,jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
import time
import threading
import urllib.request
import requests


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'hezronmontadas@gmail.com'
app.config['MAIL_PASSWORD'] = 'ixclqmppmjeilxzc'
app.config['MAIL_DEFAULT_SENDER'] = 'hezronmontadas@gmail.com'
app.config['MAIL_USE_TLS'] = False

Email = Mail(app)
model = Model()

now = datetime.now().strftime('%I:%M %p')
datetoday2 = date.today().strftime("%d-%B-%Y")
start_time = time.time()
current_date = datetime.today()
# Creating file
folderModePath= 'face_image'
if not os.path.isdir('face_image'):
    os.makedirs('face_image')

# ARRANGE FILES IMPORTED

def file_arrange(folderModePath):
    imagelist = []
    id_student = []
    imglist = os.listdir(folderModePath)
    #print(imglist)
    for path in imglist:
        imagelist.append(cv2.imread(os.path.join(folderModePath, path)))
        id_student.append(os.path.splitext(path)[0])

    return imagelist,id_student

# TRAINING FACE

def findTrain(imglist):
    encodeList = []
    for img in imglist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #resize = cv2.resize(img,(0,0), None , 0.25,0.25)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#  TRAINED FACE 

def train_faced():
    results = model.retriveTrainFaces()

    for result in results:
        encoded_face = pickle.loads(result[1])
    imgModelist, studentID = encoded_face

    return imgModelist, studentID

# STMP EMAIIL SENDER

def Email_notify(to,subject,template):
    msg = Message(subject,recipients=[to])
    msg.html = template
    Email.send(msg)

       
            


# AUTHENTICATION

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email_ad' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# OPTION 1 OF CLASSROOM UTILIZATION

def Classroon_uti():
    rooms = []
    enterClass = input("Enter a class room: ")
    room = model.Classroom() 
    for i in room:
        if i[0] == enterClass:
            print("match")
            rooms.append(i)
        else:
            print("no match")

    print(rooms)
    return rooms 


recognizing_faces = True
def face_Recognized():
    
    instructor_detected = False
    prev_data = None
    verify_data = None
    face_cascade = cv2.CascadeClassifier("Web_app/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("Web_app/haarcascade_eye.xml")
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    time_limit = 2 * 60
    rooms =  Classroon_uti()
    
       
    while recognizing_faces:
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            cap.release()
            break
        success, frame = cap.read()
        if not success:
            break
        
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5) 
        
        
        imgModelist, studentID = train_faced()

        imgS = cv2.resize(frame,(0,0), None ,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        faceCurrent = face_recognition.face_locations(imgS)
        encodedFaces = face_recognition.face_encodings(imgS,faceCurrent)
    
        for encodeface, faceloc in zip(encodedFaces,faceCurrent):
            if not instructor_detected:
                matches = face_recognition.compare_faces(imgModelist,encodeface, tolerance=0.45)
                faceDistance = face_recognition.face_distance(imgModelist,encodeface)
                matchIndex = np.argmin(faceDistance)
                if matches[matchIndex]:
                    
                    instructor = studentID[matchIndex]
                    face_recognized = model.RetrieveInstructorData(instructor)
                    face_output = face_recognized[5].replace("\r\n", "")
                    day_schedule = face_recognized[9]
                    class_start_ = face_recognized[7]
                    class_end_ = face_recognized[8]
                    #current_time = datetime.now().time()
                    #current_day = current_date.weekday()
                    #days_to_tuesday = (1 - current_day) % 7
                    #tuesday = current_date + timedelta(days=days_to_tuesday)
                    #class_start = datetime.combine(datetime.now().date(), datetime.min.time()) + class_start_
                    #class_end = datetime.combine(datetime.now().date(), datetime.min.time()) + class_end_
                    if any(room[0] == face_output for room in rooms):
                    #    print(f'Instructor face {face_recognized} with room {face_output}')
                    # OPTION 2
                    #if class_start.time() <= datetime.now() <= class_end.time():
                        print("successfull")
                        text_size, _ = cv2.getTextSize("INSTRUCOR RECOGNIZED", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        text_x = faceloc[3] * 4
                        text_y = faceloc[0] * 4 - text_size[1] - 10
                        cv2.rectangle(frame, (text_x-5, text_y-5), (text_x+text_size[0]+5, text_y+text_size[1]+5), (0,0,0), -1)
                        cv2.putText(frame, "INSTRUCOR RECOGNIZED", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                        instructor_detected = True
                        if instructor != verify_data:
                            model.Insert_time(instructor,datetime.now())
                            verify_data = instructor
                    else:
                        print("This is not your Classroom")
                else:
                    print("Instructor not found")
            else:
                matches = face_recognition.compare_faces(imgModelist,encodeface, tolerance=0.45)
                faceDistance = face_recognition.face_distance(imgModelist,encodeface)
                matchIndex = np.argmin(faceDistance)
                        
                if matches[matchIndex]:
                    student = studentID[matchIndex]
                    result = model.RetrieveData(student)
                        
                    if face_recognized[4] == result[6]:
                        if result:
                            print(f"Student face {result} matches")
                            text_size, _ = cv2.getTextSize(result[1], cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                            text_x = faceloc[3] * 4
                            text_y = faceloc[0] * 4 - text_size[1] - 10
                            cv2.rectangle(frame, (text_x-5, text_y-5), (text_x+text_size[0]+5, text_y+text_size[1]+5), (0,0,0), -1)
                            cv2.putText(frame, result[1], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                            if student != prev_data:
                                model.InsertJoin(student,datetime.now())
                                #Email_notify(result[5], 'Attendance Confirmation', f'Dear , your attendance has been confirmed. You entered the classroom at '+now+'')
                                prev_data = student
                                #print(output)
                            else:
                                print("Already confirmed face")
                        else:
                            print("Student face not in database")        
                    else:
                        print("Warning! Your on a Wrong Classroom")
                        text_size, _ = cv2.getTextSize('Warning! Unknown student', cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        text_x = faceloc[3] * 4
                        text_y = faceloc[0] * 4 - text_size[1] - 10
                        cv2.rectangle(frame, (text_x-5, text_y-5), (text_x+text_size[0]+5, text_y+text_size[1]+5), (0,0,0), -1)
                        cv2.putText(frame, 'Warning! Unknown student', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)         

                else:
                    print("student not recognized")
                    text_size, _ = cv2.getTextSize('this student not registered', cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    text_x = faceloc[3] * 4
                    text_y = faceloc[0] * 4 - text_size[1] - 10
                    cv2.rectangle(frame, (text_x-5, text_y-5), (text_x+text_size[0]+5, text_y+text_size[1]+5), (0,0,0), -1)
                    cv2.putText(frame,'this student not registered', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)


        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h), (255,0,0),2)
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+w, x:x+w]
            eye = eye_cascade.detectMultiScale(roi_gray,1.3,5)
            for (ex,ey,ew,eh) in eye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    time.sleep(5 * 60)
    recognize_faces_thread = threading.Thread(target=face_Recognized)
    recognize_faces_thread.start()
    

    


#   /// // // // // // // /// / ROUTING API // / / /// // /// /// /// // // // // //

# FACE RECOGNITION


recognize_faces_thread = threading.Thread(target=face_Recognized)
recognize_faces_thread.start()
    #time.sleep(1 * 60)

    #return redirect('/')
    

# REGISTER INFO AND TRAIN DATA
@app.route("/upload", methods=["POST","GET"])
def upload():
    imagelist,id_student = file_arrange(folderModePath)
    if request.method == "POST":
        image = request.files['image']
        id = request.form['id']
        fullname = request.form['fullname']
        email = request.form['email']
        course = request.form['course']
        year = request.form['year']
        gender = request.form['gender']
        

        filename = secure_filename(f'{id}{os.path.splitext(image.filename)[1]}')
        image.save(os.path.join(folderModePath,filename))

        imagelist.append(cv2.imread(os.path.join(folderModePath, filename)))
        id_student.append(id)

        encodeListKnown = findTrain(imagelist)
        encodeListKnownwithIds = [encodeListKnown,id_student]
      
        print(encodeListKnownwithIds)
        print("Encoding Completed")
        print("Processing.................... .. .. ")
        file = open('EncoderFile.p', 'wb')
        pickle.dump(encodeListKnownwithIds,file)
        file.close()
        model.train_face_import(id,pickle.dumps(encodeListKnownwithIds))
        print("file saved successfully")
        result = model.Insertdata(id,fullname,course,year,gender,email)
        if result == None:
            flash("Data saved successfully in Database")
    return render_template('inputdata.html') 

# REGISTER INFO AND TRAIN DATA

@app.route('/register',methods=['POST','GET'])
def register():

    facelist,instructor_id = file_arrange(folderModePath)
    if request.method == 'POST':
        file_image = request.files['image']
        id_instructor = request.form['id_instructor']
        instructor_name = request.form['fullname_instructor']
        email = request.form['email_instructor']
        password = request.form['password']
        password_hash = bycryt.generate_password_hash(password).decode('utf-8')
        re_password = request.form['re-password']
        department = request.form['department']
        subject = request.form['subject']
        if re_password != password:
            flash("You type an incorrect password.Please try again!",category='danger')
            return redirect(url_for('register'))


        filename = secure_filename(f'{id_instructor}{os.path.splitext(file_image.filename)[1]}')
        file_image.save(os.path.join(folderModePath,filename))

        facelist.append(cv2.imread(os.path.join(folderModePath, filename)))
        instructor_id.append(id_instructor)

        encodeList = findTrain(facelist)
        encodeListKnownIds = [encodeList,instructor_id]
        #print(encodeListKnownIds)
        print("Encoding Completed")
    
        print("Processing.................... .. .. ")
        files = open('EncoderFile.p', 'wb')
        pickle.dump(encodeListKnownIds,files)
        files.close()
        model.train_face_import(id_instructor,pickle.dumps(encodeListKnownIds))
        print("file saved successfully")

        result = model.InsertInstructor(id_instructor,instructor_name,email,password_hash,department,subject)
    
        if result == None:
            flash("Data saved successfully in Database",category='success')

    return render_template('register.html')



# login to the attendance web monitoring

@app.route('/')
@app.route('/login',methods=['POST','GET'])
def login():
    if 'email_ad' in session:
        # user is already logged in, redirect to dashboard page
        return redirect(url_for('index',email_ad=session['email_ad']))
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            result = model.password_check(email)
            if result:
                hashpass = result[0]
                unhashpass = bycryt.check_password_hash(hashpass,password)
                if unhashpass:
                    fetchall = model.displayInstructor(email)
                    email_address = fetchall[0]['fullname']
                    session['email_ad'] = email_address
                    session['user_id'] = fetchall[0]['instructor_id']
                    session['subject'] = fetchall[0]['subject']
                    session['department'] = fetchall[0]['Department']
                    session['schedule'] = fetchall[0]['class_time']
                    session['room'] = fetchall[0]['room']
                    model.logs_record_login(session['user_id'],datetime.now())
                    return redirect(url_for('index', email_ad=session['email_ad']))
                else:
                    flash('Invalid password',category='danger')
            else:
                flash('User Not FOund', category='danger')
            
        return render_template('login.html')
 
# logout user
@app.route('/logout')
def session_logout():
   
    if 'user_id' in session:
        model.logs_record_logout(session['user_id'])
    session.clear()
    flash('You have been logged out!', category='warning')
    return redirect(url_for('login'))


# main dashboard
@app.route('/dashboard/<email_ad>')
@login_required
def index(email_ad):
    if 'email_ad' not in session:
        #flash('You must be logged in to access this page',category='warning') 
        return redirect(url_for('login'))
    else:
        output1 = model.attendance_record(session['user_id'])
        #output1 = model.JoinStatement()
        return render_template('index.html',output1=output1,datetoday2=datetoday2,output=session['email_ad'],email_ad=email_ad,subject=session["subject"],department = session['department'],schedule = session['schedule'],room=session['room'])

# student List
 
@app.route('/studentList')
def studentList():
    if 'email_ad' not in session:
        return redirect(url_for('login'))
    result = model.student_list()
    return render_template('student_list.html',results=result)

# Register form

@app.route('/InsertData')
def trainData():
    if 'email_ad' not in session:
        return redirect(url_for('login'))
    return render_template('inputdata.html')


# Logs record

@app.route('/instructorlogs')
def logs():
    if 'email_ad' not in session:
        return redirect(url_for('login'))
    
    result = model.JoinInstructor()
    #logout = model.Joinlogout_record()
    result1 = model.joinLogsInstructor()
    return render_template('instructorlogs.html',result=result,result1=result1)

#@app.route('/classSchedule')
#def classSchedule():
#    return render_template('ClassSched.html')