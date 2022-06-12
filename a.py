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


cam = cv2.VideoCapture(0)

#Creamos un login
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__() 
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password) #Hace que la contraseña se vea como puntitos
        self.createaccbutton.clicked.connect(self.gotocreate)
    def loginfunction(self):
        email=self.email.text()
        password= self.password.text()
#         print("Ingresó correctamente con su email: ", email, "y contraseña: ", password)
    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
    def createaccfunction(self):
        email = self.email.text()
        if self.password.text()==self.confirmpass.text():
            password=self.password.text()
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
         
app = QApplication(sys.argv)
mainwindow=Login()
widget= QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(308)
widget.setFixedHeight(400)
widget.show()
app.exec_()
    

def tomar_foto():
    print("Imagen Tomada")
    ret, image = cam.read()
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
    while(True):
        ret, frame = cam.read()
        video_out.write(frame)
        if GPIO.input(16) == GPIO.LOW:
            break
    cam.release()
    video_out.release()
    print("Video Guardado en el Directorio")

    