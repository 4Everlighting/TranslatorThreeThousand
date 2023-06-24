#Assignment: Python Project 1
#Joshua Pacheco (JP), 6/04/2023, The Translator Two Thousand, Python3 project
#I am estimating this will take 3 hours to code. It actually took 4 hours to code, as I had issues 
##Spent an additional 1 hour fixing the language output to be the Spanish accent for the when it speaks spanish translation


import sys, textwrap, time
import speech_recognition as sr
from textblob import TextBlob
import pyttsx3

import time, Adafruit_GPIO.SPI as SPI, Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi_I2C_driver
from time import *
from builtins import chr

#  Set to true to silence initial welcome message
SILENT_START = False
DEBUG_TEXT = False
DISPLAY_MODE = 'lcd'
WIDTH = 20

ESPEAK_VOICE="english-mb-en1"


WELCOME_TEXT = """Hello, I am the Translator Interface Three Thousand"""
SELECTION_ROWS = ["","<-Spanish - English"," English - Spanish->"]

if DISPLAY_MODE == 'lcd':
  mylcd = RPi_I2C_driver.lcd()

if DISPLAY_MODE == 'oled':
    RST = None
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    disp.begin()
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    font = ImageFont.load_default()

#dictionary to define language based on the choice and what to speak as
lang_tr = {
    'en': "English",
    'es': "Spanish",
}


DELAY_SECONDS = 7
def block_until_enter():
    print(f"Starting delay of {DELAY_SECONDS} seconds")
    sleep(DELAY_SECONDS)
    print("Delay expired. removing translated text from display and returning to menu")


def draw_rows_on_display(ROWS):
    if DISPLAY_MODE == 'lcd':
        mylcd.lcd_clear()
        if len(ROWS) > 0:
          mylcd.lcd_display_string(ROWS[0], 1)
        if len(ROWS) > 1:
          mylcd.lcd_display_string(ROWS[1], 2)
        if len(ROWS) > 2:
          mylcd.lcd_display_string(ROWS[2], 3)
        if len(ROWS) > 3:
          mylcd.lcd_display_string(ROWS[3], 4)
    if DISPLAY_MODE == 'oled':
        disp.clear()
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),       ROWS[0],  font=font, fill=255)
        draw.text((x, top+8),     ROWS[1],  font=font, fill=255)
        draw.text((x, top+16),    ROWS[2],  font=font, fill=255)
        draw.text((x, top+24),    ROWS[3],  font=font, fill=255)
        disp.image(image)
        disp.display()

def draw_text_on_display(TEXT):
    #print(f'Converting {len(TEXT)} characters of text to rows of max length {WIDTH}: "{TEXT}"')
    ns = textwrap.wrap(TEXT,width=WIDTH)
    if DEBUG_TEXT:
      print(f'Converted {len(TEXT)} characters to {len(ns)} rows of text!')
      print(ns)

    l1=''
    l2=''
    l3=''
    l4=''
    if len(ns)>0:
        l1=ns[0]
    if len(ns)>1:
        l2=ns[1]
    if len(ns)>2:
        l3=ns[2]
    if len(ns)>3:
        l4=ns[3]

    if DISPLAY_MODE == 'lcd':
        mylcd.lcd_clear()
        mylcd.lcd_display_string(l1, 1)
        mylcd.lcd_display_string(l2, 2)
        mylcd.lcd_display_string(l3, 3)
        mylcd.lcd_display_string(l4, 4)
    if DISPLAY_MODE == 'oled':
        disp.clear()
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),       l1,  font=font, fill=255)
        draw.text((x, top+8),     l2,  font=font, fill=255)
        draw.text((x, top+16),    l3,  font=font, fill=255)
        draw.text((x, top+24),    l4,  font=font, fill=255)
        disp.image(image)
        disp.display()

#function to trabslate the text
def translate_text(text, from_lang, to_lang):
    blob = TextBlob(text)
    print(f"I am converting {from_lang} to {to_lang}")
    translated_text = blob.translate(from_lang=from_lang, to=to_lang)
    return translated_text

#function to speak the text utilizing the pyttsx3 for text to speech functionality
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

#Function that utilizes the microphone and listens for speech
display_text_es = "Habla tu Español"
display_text_en = "Speak your English"
def listen_for_speech(language):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        #draw_rows_on_display(["Habla tu español"])
        if language == 'es':
          draw_rows_on_display([display_text_es])
        elif language == 'en':
          draw_rows_on_display([display_text_en])
        print(f"Speak in {lang_tr[language]}...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language=language)
        print(f"Recognized {language} Text: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        print("Unable to recognize speech.")
        return None
    except sr.RequestError as e:
        print(f"Recognition request error: {str(e)}")
        return None


#main menu funtion
def menu():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    draw_text_on_display(WELCOME_TEXT)
    if not SILENT_START:
      engine.say("Hello, I am the Translator Interface Three Thousand. Please select from the MENU, but know soon as you you make your selection, be ready to speak in the language it tells you to speak in.")
      engine.runAndWait()
    while True:
        #print menu to the console for UX
        draw_rows_on_display(SELECTION_ROWS)
        print("1- English to Spanish\n2- Spanish to English\n3- Exit")
        #for a better user experience, It warns you to be ready to say what you want translated, in the language it needs to be spoke in
        choice = input("Be ready to speak in the language it tells you to speak in!!\nEnter your choice: ")
        #if they choose #1 to have the English to Spanish translation
        if choice == "1":
            english_text = listen_for_speech("en")
            if english_text:
                translated_text = translate_text(english_text, "en", "es")
                print(f"Translated Text: {translated_text}")
                draw_text_on_display(str(translated_text))
                #engine.setProperty('voice', voices[2].id)
                #speak_text(translated_text)
                block_until_enter()
        #if they choose choice #2 and want Spanish to English translation
        elif choice == "2":
            spanish_text = listen_for_speech("es")
            if spanish_text:
                translated_text = translate_text(spanish_text, "es", "en")
                print(f"Translated Text: {translated_text}")
                draw_text_on_display(str(translated_text))
                engine.setProperty('voice', voices[0].id)
                speak_text(translated_text)
                block_until_enter()
        elif choice == "3":
            sys.exit(0)
        else:
            #error checking for any choices other than 1-3
            print("Invalid choice. Please enter a valid choice.")

if __name__ == "__main__":
    menu()
