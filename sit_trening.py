import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
#from bs4 import BeautifulSoup
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime, timedelta
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait, Select
#from selenium.webdriver.support import expected_conditions as EC
import time
import yaml

def addBooking(booking, token):
    addBookingUrl = 'https://ibooking.sit.no/webapp/api//Schedule/addBooking'
    payload = {'token': token, 'classId': booking['id']}
    requests.post(addBookingUrl, data=payload)

#set up
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
password = os.getenv('password')
name = os.getenv('name')

with open('sit_trening.yaml') as info:
      info_dict = yaml.load(info)
if info_dict["trenigssenter"] == "Gløshaugen":
	schedulesStudio = 306
if info_dict["trenigssenter"] == "Dragvoll":
	schedulesStudio = 307
if info_dict["trenigssenter"] == "Portalen":
	schedulesStudio = 308
if info_dict["trenigssenter"] == "DMMH":
	schedulesStudio = 402
if info_dict["trenigssenter"] == "Moholt":
	schedulesStudio = 540

if password is None:
    print('env var password is None, exiting script')
    exit()
if name is None:
    print('env var name is None, exiting')
    exit()

logInUrl2 = 'https://auth.dataporten.no/accountchooser?returnTo=https%3A%2F%2Fauth.dataporten.no%2Foauth%2Fauthorization%3Fclient_id%3D93ae97a1-5633-45ac-92a0-86ba891aec02%26redirect_uri%3Dhttps%253A%252F%252Fwww.sit.no%252Foauth%252Fauthorized2%252F1%26response_type%3Dcode%26scope%3Demail%2520longterm%2520peoplesearch%2520profile%2520userid%2520userid-feide%2520userinfo%2520groups%2520phone&clientid=93ae97a1-5633-45ac-92a0-86ba891aec02'
selfWorkoutUrl = 'https://www.sit.no/trening/treneselv'

#log into sit trening Feide is hard so we choose hacky solution
browser = webdriver.Firefox() 
browser.get(logInUrl2)

username = browser.find_element_by_id('org-chooser-selectized')
username.send_keys('NTNU')
browser.find_element_by_xpath('/html/body/div/article/section[2]/form[2]/div/div[2]/div').click()
browser.find_element_by_xpath('/html/body/div/article/section[2]/form[2]/button').click()
time.sleep(1) #may crash if we dont have this
username = browser.find_element_by_id('username')
username.send_keys(name)
passw = browser.find_element_by_id('password')
passw.send_keys(password)
browser.find_element_by_xpath('/html/body/div/article/section[2]/div[1]/form/button').click()
time.sleep(3) #may crash if we dont have this
browser.find_element_by_xpath('/html/body/div[2]/div/header/div/div[2]/div/div[2]/div[2]/a[2]/span').click()
browser.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div/div/div/div/div[2]/form/div/div[1]/div/div[1]/a/span').click()
browser.find_element_by_xpath('/html/body/div/article/section[2]/ul/li/a/div/div[2]').click()
print("Logged in") 

#Booking procedure
browser.get(selfWorkoutUrl)
ibooking_iframe = browser.find_element_by_id('ibooking-iframe')
print('Booking classes')
ibooking_token = parse_qs(urlparse.urlparse(ibooking_iframe.get_attribute('src')).query)['token'][0]
getScheduleUrl = 'https://ibooking.sit.no/webapp/api/Schedule/getSchedule'
schedulePayload = {'token': ibooking_token, 'studio': schedulesStudio}

scheduleResponse = requests.post(getScheduleUrl, data=schedulePayload)
schedule = scheduleResponse.json()
while schedule['days'] == None:
	scheduleResponse = requests.post(getScheduleUrl, data=schedulePayload)
	schedule = scheduleResponse.json()

bookingDay = None
for day in schedule['days']:
    d = datetime.now() + timedelta(days=info_dict["day_ahead"])
    if day['date'] == (d.strftime('%Y-%m-%d')):
        bookingDay = day
        break
if bookingDay == None:
    print('Cannot find the day in', info_dict["day_ahead"], 'days, exiting')
    exit()
booking1 = None
for singleClass in bookingDay['classes']:
    if singleClass['studio']['name'] == info_dict["trenigssenter"]:
        if info_dict["tid"] in singleClass['from'] and singleClass['available'] > 0:
            booking1 = singleClass
            addBooking(booking1, ibooking_token)
            print('Booking complete at', d.strftime('%Y-%m-%d'), info_dict["tid"], info_dict["trenigssenter"])
            exit()

if booking1 is None:
    print("Cannot find booking, exiting")
    exit()

