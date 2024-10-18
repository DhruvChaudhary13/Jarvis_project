import speech_recognition as sr  ## here sr is used as alias for speech recognition
import webbrowser
import pyttsx3       ## this is a library which is used to convert text to speech
import sphinx
import pyaudio
import musiclibrary
import sys    # a library that is used to interact with python interpreter
import requests
from google.cloud import aiplatform
import google.generativeai as genai
import os
import export
import google.auth
import cv2



GOOGLE_API_KEY="AIzaSyDyXqrkRp11y9mwurjsyUPmF7wtkAI6x_Q"
genai.configure(api_key = os.environ.get(GOOGLE_API_KEY))



# funct
def aiprocess(command):
    
    genai.configure(api_key = os.environ.get(GOOGLE_API_KEY))
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
            {"role": "user", "parts":command }
        ]
    )
    
    # Send the user's command to the chat and get the response
    response = chat.send_message(command)
    
    # Return the content of the first choice in the response
    return response.choices[0].history.content
   


def cam_open(command):
    video_cap = cv2.VideoCapture(0)

    while True:
        ret, vido_data = video_cap.read()  # Capture a video frame
        
        cv2.imshow("vido_live", vido_data)  # Display the frame in a window vdo_live si the frame and the data cature will got videodata which is then readed

        # Break the loop if the 'a' key is pressed
        if cv2.waitKey(5) == ord("e"):
            break

    # Release the video capture object and close the display window
    video_cap.release()
    cv2.destroyAllWindows()   

   

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# api key for news api
apikey="60c3055ad0eb43e4b4f6b9b941b5fc0c"
url=f"https://newsapi.org/v2/top-headlines?country=india&apiKey={apikey}" 



# function to speek the text
def speak(text):
   engine.say(text)
   engine.runAndWait()
   
def process_command(c):  #here we define c variable which will will store value of command
   if "open google" in c.lower():
      webbrowser.open("https://google.com")
   
   elif "play news" in c.lower():
       r=requests.get(url)
       if r.status_code==200:
           data=r.json()
       # extract the articles

           articles=data.get('articles',[])     #here article will become a list whicb contain contain all the articles coming from api
           for article in articles:
               speak(article['title'])
   
   elif c.lower().startswith("open camera"):
    speak("opening camera sir")
    cam_open(c)

   elif c.lower().startswith("play"):
      song=c.lower().split(" ")[1]
      link=musiclibrary.music[song]
      webbrowser.open(link)
   
   elif "shutdown" in c.lower():
      speak("signing off")
      sys.exit()   # this function is used to exit the program
   
   else:
      output=aiprocess(c)
      speak(output)

      

if __name__== "__main__":
    
    speak("intializing Jarvis......")    
    # speak("hello sir")
    while True:
      # listen audio from the wake word " jarvis"
      # obtain audio from microphone 
      r=sr.Recognizer()
      with sr.Microphone() as source:
        print("listening....")
        audio = r.listen(source) # here source is microphone which takes audio and save it to audio
        Timeout:2
        phrase_time_limit:2  # if there is no voice coming then code will exit in 5 sec

      #  recognize speech using Sphinx
      try:
            word = r.recognize_google(audio)
            print(word)  
            if(word.lower()=="hello"):  # .lower() is used for string handling
              #  print(command)

                speak("yes sir")
                # listen for commmand
                with sr.Microphone() as source:
                   print("activating sir")
                   audio = r.listen(source)  
                   command = r.recognize_google(audio)
                   
                   process_command(command) # function calling for the command 
                


      except sr.UnknownValueError:
        print(" sphinx could not understand audio")
      except sr.RequestError as e:
         print("sphinx error; {0}", format(e))







 

 







                                      
                                       
                                           
                                                  
                                                    




