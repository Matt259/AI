from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPlainTextEdit, QMessageBox
import sys
import smtplib
from email.message import EmailMessage
from functions import spotify, wiki, google, youT, joke
from Voice import talk, get_Command, predict
#from validation import check_empty_reg, password_match, check_matching_data, register_user


#Email window class
class EmailWindow(QMainWindow):
    #Email window constructor
    def __init__(self):
        super(EmailWindow, self).__init__()
        self.setGeometry(400,400,400,400)
        self.setWindowTitle("Email sender")
        self.initUI()

    #Init GUI
    def initUI(self):
        self.b1 = QtWidgets.QPushButton("Send Mail", self)
        self.b1.move(10,360)
        self.b1.clicked.connect(self.is_text_empty)

        self.b2 = QtWidgets.QPushButton("Back", self)
        self.b2.move(120,360)
        self.b2.clicked.connect(self.back_to_MyWindow)

        self.receiver = QLineEdit(self)
        self.receiver.setPlaceholderText("Receiver")
        self.receiver.move(10, 20)
        self.receiver.resize(280, 25)

        self.subject = QLineEdit(self)
        self.subject.setPlaceholderText("Subject")
        self.subject.move(10, 60)
        self.subject.resize(350, 25)

        self.message = QPlainTextEdit(self)
        self.message.move(10, 100)
        self.message.resize(350, 200)

    #Function to go back to the main screen
    def back_to_MyWindow(self):
        self.myWindow = MyWindow()
        self.myWindow.show()
        self.close()

    def is_text_empty(self):

        if self.receiver.text().replace(" ", "") and self.message.toPlainText().replace(" ", "") != "":
            receiver = self.receiver.text()
            subject = self.subject.text()
            message = self.message.toPlainText()
            self.send_mail(receiver,subject,message)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Missing subject or message')
            msg.setWindowTitle("Error")
            msg.exec_()


    def send_mail(self,receiver,subject,message):

        EMAIL_ADDRESS = 'matas.mik392@go.kauko.lt'
        EMAIL_PASS = 'jfrsyjjrgbgysubz'

        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.set_content(message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
            smtp.send_message(msg)




class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.setGeometry(500, 500, 240, 250)
        self.setWindowTitle("Virtual Assistant register")
        self.initUI()

    def initUI(self):
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.move(10, 20)
        self.username.resize(220, 25)

        self.email = QLineEdit(self)
        self.email.setPlaceholderText("Email")
        self.email.move(10, 60)
        self.email.resize(220, 25)

        self.pwd = QLineEdit(self)
        self.pwd.setPlaceholderText("Password")
        self.pwd.move(10, 100)
        self.pwd.resize(220, 25)

        self.pwdR = QLineEdit(self)
        self.pwdR.setPlaceholderText("Repeat Password")
        self.pwdR.move(10, 140)
        self.pwdR.resize(220, 25)

        self.b1 = QtWidgets.QPushButton("Register", self)
        self.b1.move(10, 180)
        self.b1.clicked.connect(self.register_prompt)

   # def register_prompt(self):
        #username = self.username.text()
        #email = self.email.text()
        #pwd = self.pwd.text()
       # pwdR = self.pwdR.text()

        #pwdCheck = password_match(pwd,pwdR)
        #checkEmpty = check_empty_reg(username,email,pwd,pwdR)
        #checkMatch = check_matching_data(username,email)
        #if pwdCheck and checkEmpty:
           # register_user(username, email, pwd)
        #if checkEmpty == False:
            #msg = QMessageBox()
            #msg.setIcon(QMessageBox.Critical)
            #msg.setText("Error")
            #msg.setInformativeText('Please fill everything out')
            #msg.setWindowTitle("Error")
            #msg.exec_()

        #if pwdCheck == False:
            #msg = QMessageBox()
            #msg.setIcon(QMessageBox.Critical)
            #msg.setText("Error")
            #msg.setInformativeText('Make sure the passwords match')
            #msg.setWindowTitle("Error")
            #msg.exec_()

        #if checkMatch == False:
           # msg = QMessageBox()
           # msg.setIcon(QMessageBox.Critical)
           # msg.setText("Error")
           # msg.setInformativeText('Username or Email already taken')
           # msg.setWindowTitle("Error")
           # msg.exec_()






class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 350, 350)
        self.setWindowTitle("Virtual Assistant")
        self.initUI()


    def initUI(self):
        self.b1 = QtWidgets.QPushButton("Activate", self)
        self.b1.clicked.connect(self.execute)

    def execute(self):
        talk("Hello daddy, how may I help you")
        while True:
            command = get_Command()
            prob, tag = predict(command)

            if tag == "exit":
                talk("Bye!")
                break

            if prob.item() > 0.75:

                if tag == 'spotify':
                    spotify()

                if tag == "Joke":
                    a_joke = joke()
                    talk(a_joke)

                if tag == 'google':
                    talk("What would you like me to google")
                    google_command = get_Command()
                    google(google_command)

                if tag == 'wiki':
                    talk("What would you like me to wiki")
                    wiki_command = get_Command()
                    wiki(wiki_command)

                if tag == 'youtube':
                    talk("What should I type in the search field")
                    yout_command = get_Command()
                    youT(yout_command)

                if tag == 'mail':
                    self.emailWin = EmailWindow()
                    self.emailWin.show()
                    self.close()
                    break

                talk("what else can I do for you")

            else:
                talk("Sorry, can't do that")


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    #Actually shows the window
    win.show()
    sys.exit(app.exec_())


window()
