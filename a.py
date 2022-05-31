import os
import time
import datetime
from datetime import date, time
from datetime import datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import cv2
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


pin = 11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
cam = cv2.VideoCapture(0)

#Creamos un login
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__() 
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        #self.password.setEchoMode(QtWidgets.QLineEdit.Password) #Hace que la contraseña se vea como puntitos
    def loginfunction(self):
        email=self.email.text()
        password= self.password.text()
        print("Ingresó correctamente con su email: ", email, "y contraseña: ", password)
         
app = QApplication(sys.argv)
mainwindow=Login()
widget= QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(488)
widget.setFixedHeight(620)
widget.show()
app.exec_()
    

def tomar_foto():
    print("Imagen Tomada")
    GPIO.output(pin, GPIO.LOW)
    sleep(0.1)
    GPIO.output(pin, GPIO.HIGH)
    ret, image = cam.read()
    horaf = datetime.now().strftime('%H:%M:%S')
    fechaf = datetime.now().strftime("%d-%m-%y")
    onlyfilesF = next(os.walk('/home/grupo5/Desktop/Fotos'))[2]
    nf = int(len(onlyfilesF))+1
    cv2.imwrite("/home/grupo5/Desktop/Fotos/"+str(nf)+"_"+horaf+fechaf+".jpg", image)
    sleep(4)
    print("Imagen Tomada")
        
def grabar_video():
    cam = cv2.VideoCapture(0)
    horav = datetime.now().strftime('%H:%M:%S')
    fechav = datetime.now().strftime("%d-%m-%y")
    onlyfilesV = next(os.walk('/home/grupo5/Desktop/Videos'))[2]
    nv = int(len(onlyfilesV))+1
    video_cod = cv2.VideoWriter_fourcc(*'XVID')
    video_out = cv2.VideoWriter("/home/grupo5/Desktop/Videos/"+str(nv)+"_"+horav+fechav+'.avi', video_cod, 10, (640,480))
    print("Grabando ")
    GPIO.output(pin, GPIO.LOW)
    sleep(0.1)
    GPIO.output(pin, GPIO.HIGH)
    while(True):
        ret, frame = cam.read()
        video_out.write(frame)
        if GPIO.input(16) == GPIO.LOW:
            break
    cam.release()
    video_out.release()
    print("Video Guardado en el Directorio")

    