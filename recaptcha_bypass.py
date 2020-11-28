import os
import random
import sys
import time
import urllib
import pydub
import speech_recognition
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#basic information
print('sys.argv[0] =', sys.argv[0])             
data_path = os.path.dirname(sys.argv[0])
print("path =", data_path)
browser = webdriver.Chrome(r"C:\Users\dariu\Desktop\recaptcha_bypass\chromedriver.exe")
browser.get("https://www.google.com/recaptcha/api2/demo")

#start the audio challenge
main_frame = browser.find_element_by_tag_name("iframe")
browser.switch_to.frame(main_frame)
time.sleep(random.uniform(2,5))
browser.find_elements_by_class_name("recaptcha-checkbox-border")[0].click()
browser.switch_to_default_content()

#get names of all iframes
iframes = browser.find_elements_by_tag_name("iframe")
frames = []
for iframe in iframes:
    name = iframe.get_attribute("name")
    frames.append(name)
    print(f"[+ Found iFrame: {name}]")
print(f"Found the needed frame: {frames[2]}")

#use the found name to focus the correct iframe
frame1 = frames[2]
browser.switch_to.frame(frame1)
time.sleep(random.uniform(2,5))
browser.find_elements_by_id("recaptcha-audio-button")[0].click()
browser.switch_to_default_content()
time.sleep(random.uniform(2,5))

#check for new iframes
iframes2 = browser.find_elements_by_tag_name("iframe")
frames2 = []
for iframe2 in iframes2:
    name = iframe2.get_attribute("name")
    frames2.append(name)
    print(f"[+ Found iFrame: {name}]")

#use the newly received name to access the correct iframe
frame2 = frames2[2]
browser.switch_to.frame(frame2)
time.sleep(random.uniform(2,5))
browser.find_elements_by_class_name("rc-audiochallenge-tdownload-link")[0].click()

#get the audio file
src = browser.find_element_by_id("audio-source").get_attribute("src")
urllib.request.urlretrieve(src, data_path + "\\audio.mp3")
sound = pydub.AudioSegment.from_mp3(data_path + "\\audio.mp3").export(data_path + "\\audio.wav", format="wav")

#translate the audio file into text
recognizer = speech_recognition.Recognizer()
google_audio = speech_recognition.AudioFile(data_path + "\\audio.wav")
with google_audio as source:
    audio = recognizer.record(source)
text = recognizer.recognize_google(audio, language='de-DE')
print("Recaptcha Text: {}".format(text))

#redirect the translated text into the google form
inputfield = browser.find_elements_by_id("audio-respone")
inputfield.send_keys(text.lower())
inputfield.send_keys(Keys.ENTER)
