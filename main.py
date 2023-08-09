#  website = www.flyingdeck.blogspot.com


__author__ = "Sourabh Sheokand"
__copyright__ = "Copyright 2007, The Third eye project "
__credits__ = ["Sourabh Sheokand ", "Arun Sheokand "]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Sourabh Sheokand"
__email__ = "sourabhsheokand945@gmail.com"
__status__ = "Production"


import pyttsx3
import speech_recognition as sr
import datetime
import time
import os
import PyPDF2
import smtplib
import pywhatkit
import requests
import serial
import cv2
from bs4 import BeautifulSoup
import pytesseract as tess
from PIL import Image
from codecs import decode

tess.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

 
def speak(audio,type = 'male'):
    if type=='male':
        type=0
    elif type=='female':
        type=1
    
    engine.setProperty('voice',voices[type].id)
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good Morning Sir!")
        print("Good Morning Sir!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")
        print("Good Afternoon Sir!")

    else: 
        speak("Good Evening Sir!")
        print("Good Evening Sir!")
        
    speak("I am david ,your assistant . Please tell me how may I help you")


def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        speak("Recognizing...")
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said : {query}\n")

    except Exception as e:
        print("Can't recogniziation...")
        speak("Sorry sir i can't understand please say that again ")
        return "None"
    return query


def imagerecognization():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Camera")
    img_counter = 0
    while True:
        ret,frame = cam.read()
        if not ret:
            print("Failed to grap frame")
            break
        cv2.imshow("Camera",frame)
        k = cv2.waitKey(1)
        if k%256 == 32:
            img_name = "image_number_{}.png".format(img_counter)
            cv2.imwrite(img_name,frame)
            print(f"{img_name} Written!")
            speak("Image captured...")
            cam.release()
        cv2.destroyAllWindows
    # img = Image.open('text.png')
    text = tess.image_to_string(img_name)
    print(text)
    speak("The text on the image is , {}".format(text))


def  sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('you email','password')
    server.sendmail('you email',to,content)
    server.close()


def arduinodata():
    arduino = serial.Serial('COM4',9600)
    time.sleep(2)
    distance = []
    d=0
    while d < 4:
        count = arduino.readline()
        count = decode(count)
        st = count[0:1]
        distance.append(st)
        d=d+1

    f=distance[0]
    b=distance[1]
    r=distance[2]
    l=distance[3]

    if f == 'f' or b == 'b' or r == 'r' or l == 'l':
        if f == 'f':
            if b == 'b':
                if r == 'r':
                    if l == 'l':
                        print("stop")
                        speak("Sir please stop and walk carefully you are surronded by my object from all sides.")
                    else:
                        print("turn left")
                        speak("sir turn left side , you surronded by objects except in left direction.")
                else:
                    print("turn left or right ")
                    speak("sir please turn left or right , something is coming from the back and there is a object infront of you.")
            else:
                print("object is found in the path")
                speak("Sir there is an object in the path")

        elif b == 'b':
            if r == 'r':
                if l == 'l':
                   print("Move faster.") 
                   speak("Move faster and you can't turn and something coming from the back.")
                else:
                    print("turn left.")
                    speak("Turn left some thing is coming from the back.")
            else:
                print("trun left or right")
                speak("Something is coming from the back and you can turn both sides.")

        elif r == 'r':
            if l== 'l':
                print("don't turn")
                speak("Move forward only , on both right and left side object is found")
            else:
                print("don't turn right")
                speak("A object is found on right side")

        else:
            print("on left side object is found")
            speak("A object is found on right side")


def googleassistance(query):
    user_query = query
    URL = "https://www.google.co.in/search?q="+user_query
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    page = requests.get(URL,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    result = soup.find(class_='qrShPb kno-ecr-pt PZPZlf mfMhoc').get_text()
    return result


def partner():
    print("Lina bot Start>>>")
    speak('''Hello Sir! I am Lina and he is my partner Sourabh . 
    And we are from K.M. College , Narwana
     and today we repesent this modal based upon the sensor technology and smart api 
    And we made this for blind people to help them to explore this world and 
    with the help of this they can make our life more comfortable.
    And this is a fully function modal. ''',"female")


def readbook():
    book = open('introduction to electrodynamics ( PDFDrive ).pdf','rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    page = pdfReader.getPage(1)
    text = page.extractText()
    print(text)
    speak("Start Reading the book :")
    speak(text)
    speak("End of the first page.")
    speak("End of the book.")


def wikipedia():
    speak('Sir! what did you wanted to search on wikipedia.')
    query = takeCommand()
    result = wikipedia.summary(query,sentence=2)
    speak("According to wikipedia...")
    print(result)
    speak(result)


def location():
    speak("Your current location is ")
    speak("Narwana")
    print("narwana")

def opengoogle():
    try:
        speak("Sir ! what did you wanted to search.")
        ser = takeCommand()
        print(f"User said : {ser}")
        result = googleassistance(ser)
        print(result)
        speak(result)
    except Exception:
        print("Sorry sir no result is found")
        speak("sorry sir no result is found. please try another thing")


def playmusic():
    music_dir = 'D:\Music'
    songs = os.listdir(music_dir)
    print("open list")
    print(f"song : {songs[15]}")
    os.startfile(os.path.join(music_dir,songs[15]))


def date():
    Date = datetime.date.today()
    Day = Date.weekday()
    daylist = ['monday' ,'tuesday','wednesday','thursday','friday','saturday','sunday']
    print("Date= ")
    print(Date)
    print(daylist[Day])
    speak(Date)
    speak(daylist[Day])


def nowtime():
    tm = datetime.datetime.now().strftime('%H %M %S')
    speak(tm)


def email():
    try:
        print('taking content...')
        speak('what should i say?')
        content = takeCommand()
        to = 'sourabhsheokand945@gmail.com'
        sendEmail(to,content)
        print("Email has been sent!")
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry! sir i can't send the mail.")


def sendmessage():
    pywhatkit.sendwhatmsg_instantly("your number","Hello Sir!\n kasa laga sir modal")
    pywhatkit.sendwhatmsg_instantly("","hello\nWhat up sir\nkasa lag model")
    speak("Message sent!")


def explanition():
    print("-----------------------------------------------explanition start-----------------------------------------------------------")
    speak('''This modal mainly constist of two parts 
    one of them was sensor part which help to the blind people to detect any object in its path
     and done with the help of utlrasonic sensors which able to detect any object in all four directions 
     and this help the blind people or those people who don't see properly.
     And the second part of this model is the voice based assistant ,David
    and it help blind people to alot in interface with any type of software and websurfing 
    and i can do a lot of things like telling the date and time , send mails , search on web browser , send whatsapp messages , tell location , read book for blind people
           and at last it can also convert a real time  image into audio and this help blind people alot ''',"female")
    time.sleep(1)
    speak('''let Now we talk about the functionality of software''',"female")
    print("--------------------------------------------Start testing the software------------------------------------------------------")
    speak("date","female")
    date()
    time.sleep(1)
    speak("time","female")
    nowtime()
    time.sleep(1)
    speak("send message","female")
    sendmessage()
    time.sleep(1)
    speak("location","female")
    location()
    time.sleep(1)
    speak("open google","female")
    speak("Madam ! what did you wanted to search")
    speak("capital of india","female")
    speak("New Delhi")
    time.sleep(1)
    speak("Now we change a real time  image into a audio for blind people.","female")
    speak("And sorry also because the camera of the laptop is not so good","female")
    speak("and we use auto filled images to use this module ","female")
    speak("show image ","female")
    imagerecognization()
    time.sleep(1)
    speak("read book","female")
    readbook()
    time.sleep(1)
    speak("now you can test the functionality of software","female")
    speak("i again open it for you","female")
 

if __name__=="__main__":
    end = 0
    partner()
    explanition()
    time.sleep(2)
    print("-----------------------------------------------David Assistant Boot up-------------------------------------------------------")
    wishMe()
    while True:
         
        arduinodata()

        query = takeCommand().lower()

        if 'open google' in query:
            arduinodata()
            opengoogle()

        elif 'open wikipedia' in query:
            arduinodata()
            wikipedia()

        elif 'play music' in query:
            arduinodata()
            playmusic() 

        elif 'date' in query:
            arduinodata()
            date()
        
        elif 'time' in query:
            arduinodata()
            nowtime()

        elif 'send email' in query:
            arduinodata()
            email()

        elif 'read book' in query:
            arduinodata()
            readbook()

        elif 'show image' in query:
            arduinodata()
            imagerecognization()

        elif 'location' in query:
            arduinodata()
            location()

        elif 'send message' in query:
            arduinodata()
            sendmessage()

        elif 'explain again' in query:
            arduinodata()
            explanition()

        elif 'stop' in query:
            speak("now the software is on switch off mode")
            end =1
            break

        else:
            arduinodata()


while end == 1:
  speak("Now i am only tell you about the object in the path")
  arduino = serial.Serial('COM4',9600)
  time.sleep(2)
    
  while True:
    arduino = serial.Serial('COM4',9600)
    time.sleep(2)
    distance = []
    d=0
    while d < 4:
        count = arduino.readline()
        count = decode(count)
        st = count[0:1]
        distance.append(st)
        d=d+1

    f=distance[0]
    b=distance[1]
    r=distance[2]
    l=distance[3]

    if f == 'f' or b == 'b' or r == 'r' or l == 'l':
        if f == 'f':
            if b == 'b':
                if r == 'r':
                    if l == 'l':
                        print("stop")
                        speak("Sir please stop and walk carefully you are surronded by my object from all sides.")
                    else:
                        print("turn left")
                        speak("sir turn left side , you surronded by objects except in left direction.")
                else:
                    print("turn left or right ")
                    speak("sir please turn left or right , something is coming from the back and there is a object infront of you.")
            else:
                print("object is found in the path")
                speak("Sir there is an object in the path")

        elif b == 'b':
            if r == 'r':
                if l == 'l':
                   print("Move faster.") 
                   speak("Move faster and you can't turn and something coming from the back.")
                else:
                    print("turn left.")
                    speak("Turn left some thing is coming from the back.")
            else:
                print("trun left or right")
                speak("Something is coming from the back and you can turn both sides.")

        elif r == 'r':
            if l== 'l':
                print("don't turn")
                speak("Move forward only , on both right and left side object is found")
            else:
                print("don't turn right")
                speak("A object is found on right side")

        else:
            print("on left side object is found")
            speak("A object is found on right side")