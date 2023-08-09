import mysql.connector
from datetime import datetime

# STUDENT QUERIES
class Model:

    def __init__(self):
        self.connect()
       

    def connect(self):
        self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="web_app"
            )

        self.cursor = self.db.cursor()
        

    def __del__(self):
        self.cursor.close()
        self.db.close()
    
    def reconnect(self):
        self.db.reconnect()



    def Insertdata(self,id,fullname,course,year,gender,email):
        try:
            sql = "INSERT INTO student_main (student_id,full_name,course,year_level,gender,email_ad) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (id,fullname,course,year,gender,email)
            self.cursor.execute(sql,values)
            self.db.commit()
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.Insertdata(id, fullname, course, year, gender, email)
            else:
                raise

    def InsertInstructor(self,id,fullname,email,password,department,subject):
        try:
            sql = "INSERT INTO instructor_main (instructor_id,fullname,email_ad,password,Department,subject) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (id,fullname,email,password,department,subject)
            self.cursor.execute(sql,values)
            self.db.commit()
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.InsertInstructor(id,fullname,email,password,department,subject)
            else:
                raise

    def RetrieveData(self,name):
        try:
            self.cursor.execute("SELECT student_id,full_name,course,year_level,gender,email_ad,student_subject FROM student_main WHERE student_id = %s",([name]))
            result = self.cursor.fetchone()
            if result is not None:
            # If a matching record is found, return the result
                return result
            else:
            # If no matching record is found, return an error message
                return "No matching record found"
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.RetrieveData(name)
            else:
                raise
    

    def InsertJoin(self,info,datetime):
        try:
            sql = "INSERT INTO at_attendance(student_id,at_time) VALUES (%s,%s)"
            value = (info,datetime)
            self.cursor.execute(sql,value)
            self.db.commit()
            #self.cursor.close()
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.InsertJoin(info,datetime)
            else:
                raise

    def retriveTrainFaces(self):
        try:    
            self.cursor.execute("SELECT id_person,face_trained FROM face_record")
            results = self.cursor.fetchall()

            return results
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.retriveTrainFaces()
            else:
                raise


    def RetrieveInstructorData(self,name):
        try:
            self.cursor.execute("SELECT instructor_id, fullname, email_ad, Department, subject, room, class_time,time_in,time_out,day_sched FROM instructor_main WHERE instructor_id = %s",([name]))
            result = self.cursor.fetchone()
            if result is not None:
            # If a matching record is found, return the result
                return result
            else:
            # If no matching record is found, return an error message
                return "No matching record found"
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.RetrieveInstructorData(name)
            else:
                raise

    def password_check(self,email):
        try:
            sql = "SELECT password FROM instructor_main WHERE email_ad = %s"
            val = ([email])
            self.cursor.execute(sql,val)
            result = self.cursor.fetchone()
            #self.cursor.close()
            return result
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.password_check(email)
            else:
                raise

    def displayInstructor(self,email):
        try:    
            self.cursor.execute("SELECT instructor_id,fullname,Department,subject, room, class_time FROM instructor_main WHERE email_ad = %s",([email]))
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in results:
                rows.append(dict(zip(columns, row)))
            return rows
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.displayInstructor(email)
            else:
                raise

    def JoinInstructor(self):
        try:
            self.cursor.execute('SELECT instructor_main.instructor_id, instructor_main.fullname,DATE_FORMAT(face_attendance.login_time, "%h:%i %p") as login_time FROM instructor_main INNER JOIN face_attendance ON instructor_main.instructor_id = face_attendance.instructor_id')
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in results:
                rows.append(dict(zip(columns, row)))
            return rows
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.JoinInstructor()
            else:
                raise


    def Insert_time(self,info,datetime):
        try:
            sql = "INSERT INTO face_attendance(instructor_id,login_time) VALUES (%s,%s)"
            value = (info,datetime)
            self.cursor.execute(sql,value)
            self.db.commit()
            #self.cursor.close()
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.Insert_time(info,datetime)
            else:
                raise

    def train_face_import(self,id,faces):
        try:
            sql = "INSERT INTO face_record(id_person,face_trained) VALUES (%s,%s)"
            value = (id,faces)
            self.cursor.execute(sql,value)
            self.db.commit()

        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.train_face_import(id,faces)
            else:
                raise

    def student_list(self):

        try:
            self.cursor.execute("SELECT * FROM student_main")
            result =self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in result:
                rows.append(dict(zip(columns, row)))
            return rows
        except mysql.connector.OperationalError as e:
            if "MySQL Connection not available" in str(e):
                self.reconnect()
                self.student_list()
            else:
                raise

    def logs_record_login(self,id,timeIN):

        try:
            sql = "INSERT INTO admin_attendance (instructor_id,login_time) VALUES (%s,%s)"
            val = (id,timeIN)
            self.cursor.execute(sql,val)
            self.db.commit()
        except mysql.connector.errors.OperationalError as e:

            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.logs_record_login(id,timeIN)
            else:
                raise
    
    def logs_record_logout(self,id):
        try:
            sql = '''UPDATE admin_attendance SET logout_time = %s WHERE instructor_id = %s AND logout_time IS NULL'''
            val = (datetime.now(),id)
            self.cursor.execute(sql,val)
            self.db.commit()

        except mysql.connector.errors.OperationalError as e:

            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.logs_record_logout(id)
            else:
                raise

    def joinLogsInstructor(self):

        try:
            self.cursor.execute('SELECT instructor_main.instructor_id, instructor_main.fullname, DATE_FORMAT(admin_attendance.login_time, "%h:%i %p") as login_time, DATE_FORMAT(admin_attendance.logout_time, "%h:%i %p") as logout_time FROM instructor_main LEFT JOIN admin_attendance ON instructor_main.instructor_id = admin_attendance.instructor_id;')
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in results:
                rows.append(dict(zip(columns, row)))
            return rows
        except mysql.connector.errors.OperationalError as e:
            if "MySQL Connection not available." in str(e):
                self.reconnect()
                self.JoinInstructor()
            else:
                raise

    def JoinStatement(self):
        try:
            self.cursor.execute("SELECT student_main.full_name,student_main.course,student_main.year_level, DATE_FORMAT(at_attendance.at_time, '%h:%i %p') as attendance_time FROM student_main INNER JOIN at_attendance ON student_main.student_id = at_attendance.student_id")
            result = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in result:
                rows.append(dict(zip(columns, row)))
            #cursor.close()
            return rows
        except mysql.connector.errors.OperationalError as e:
            print(f"Error: {e}. Reconnecting to the MySQL server...")
            self.db.reconnect(attempts=3, delay=5)
            self.cursor = self.db.cursor()
            return self.JoinStatement()
        
    def attendance_record(self,name):
        try:
            self.cursor.execute("SELECT student_main.full_name,student_main.course,student_main.year_level,student_main.student_subject,instructor_main.room,instructor_main.class_time,DATE_FORMAT(at_attendance.at_time, '%h:%i %p') as timeIN FROM instructor_main INNER JOIN student_main ON instructor_main.subject=student_main.student_subject INNER JOIN classroom ON classroom.rooms=instructor_main.id_room INNER JOIN at_attendance ON student_main.student_id = at_attendance.student_id WHERE instructor_main.instructor_id = %s",(name,))
            result = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in result:
                rows.append(dict(zip(columns, row)))
            #cursor.close()
            return rows
        except mysql.connector.errors.OperationalError as e:
            print(f"Error: {e}. Reconnecting to the MySQL server...")
            self.db.reconnect(attempts=3, delay=5)
            self.cursor = self.db.cursor()
            return self.attendance_record(name)
        
    def validate_student_fr(self,instructor):
        try:
            self.cursor.execute("SELECT instructor_main.subject,instructor_main.instructor_id,student_main.student_id FROM instructor_main INNER JOIN student_main ON instructor_main.subject = student_main.student_subject WHERE instructor_main.instructor_id = %s",([instructor]))
            result = self.cursor.fetchall()
            
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in result:
                rows.append(dict(zip(columns, row)))
            #cursor.close()
            return rows
        except mysql.connector.errors.OperationalError as e:
            print(f"Error: {e}. Reconnecting to the MySQL server...")
            self.db.reconnect(attempts=3, delay=5)
            self.cursor = self.db.cursor()
            return self.validate_student_fr(instructor)   
         
    def retrieve_student_data(self):
        try:
            self.cursor.execute("SELECT student_subject FROM student_main")
            result = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in result:
                rows.append(dict(zip(columns, row)))
            #cursor.close()
            return rows
        except mysql.connector.errors.OperationalError as e:
            print(f"Error: {e}. Reconnecting to the MySQL server...")
            self.db.reconnect(attempts=3, delay=5)
            self.cursor = self.db.cursor()
            return self.validate_student_fr()
         
    def Classroom(self):
        try:
            self.cursor.execute("SELECT rooms FROM classroom")
            result = self.cursor.fetchall()
         
            return result
        except mysql.connector.errors.OperationalError as e:
            print(f"Error: {e}. Reconnecting to the MySQL server...")
            self.db.reconnect(attempts=3, delay=5)
            self.cursor = self.db.cursor()
            return self.Classroom()
         


    
#DATE_FORMAT(CONVERT_TZ(NOW(), '+00:00', '+12:00'),'%h:%i %p') AS ph_time_12h
#SELECT instructor_main.fullname,student_main.full_name,student_main.student_subject  FROM instructor_main INNER JOIN student_main ON instructor_main.subject=student_main.student_subject
"""
SELECT instructor_main.fullname,student_main.full_name,student_main.student_subject,instructor_main.room,instructor_main.class_time  FROM instructor_main INNER JOIN student_main ON instructor_main.subject=student_main.student_subject INNER JOIN classroom ON classroom.rooms=instructor_main.id_room
"""
"""
SELECT instructor_main.fullname,student_main.full_name,student_main.student_subject,instructor_main.room,instructor_main.class_time,at_attendance.at_time  FROM instructor_main 
INNER JOIN student_main ON instructor_main.subject=student_main.student_subject 
INNER JOIN classroom ON classroom.rooms=instructor_main.id_room
INNER JOIN at_attendance ON student_main.student_id = at_attendance.student_id WHERE instructor_main.instructor_id=1803042
"""
