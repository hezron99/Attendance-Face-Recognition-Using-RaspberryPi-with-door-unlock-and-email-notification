from flask import Flask

#import serial
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] ='1010101010secretkey'
#arduino = serial.Serial('COM3', 9600)
bycryt = Bcrypt(app)





from Web_app import face_recognze