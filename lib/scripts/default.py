# For config file
import json
# To delete files
import os
#Database (python in-built)
import sqlite3
# GUI
from tkinter import *
from tkinter import font, messagebox,ttk,filedialog
# Nepal standard time (Local time)
import pytz
import time
from datetime import datetime
# GUI Icon
from PIL import Image,ImageTk
# for Web Scraping 
import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
# Selelium for bot and dymanic website scraping
import selenium
from selenium import webdriver # chrome driver
from selenium.webdriver.common.by import By # finding elements by 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import ElementNotInteractableException , NoSuchElementException,TimeoutException,WebDriverException
from selenium.webdriver.support import expected_conditions as EC #For explicit waits
#For Captcha
import pytesseract
#Image Manipultion
import cv2
# Unzip File
import zipfile 
# For Checking Driver In Dict
from pathlib import Path
# Downloading Driver 
import urllib.request
# For Checking Chrome Version
import subprocess
# For fetching all file in in folder
import glob 
# For folder
import shutil






#Config File
with open ("./data/config.json","r") as read_config:
    Config=json.load(read_config)


#Fonts
font_btn = ("Arial",10)
font_lb = ("Arial",10)

# header for scraping 
Nepalstock_Header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.nepalstock.com",
    "Pragma": "no-cache",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
Nepsealpha_Header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    'Accept-Language': "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "nepsealpha.com",
    "Pragma": "no-cache",
    "Referer": "https://nepsealpha.com/trading/chart",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}


# X-PATH

market_status_xpath = "/html/body/div[2]/div[5]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/span[2]"

client_code_field_xpath= "/html/body/app-root/app-login/div/div/div[2]/form/div[1]/input"
password_field_id ="password-field"
captcha_field_id ="captchaEnter"
login_btn_xpath ="/html/body/app-root/app-login/div/div/div[2]/form/div[4]/input"

latest_buy_offer_xpath = '/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/div/div[1]/span/div/div[1]/div/table/tbody/tr[1]/td[3]'

dropdown_xpath = "/html/body/app-root/tms/app-menubar/aside/nav/ul/li[10]/a"

buysell_hyperlink_xpath = "/html/body/app-root/tms/app-menubar/aside/nav/ul/li[10]/ul/li[1]/a"

toogle_sell_xpath = "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[1]"
toogle_buy_xpath = "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[3]"

script_field_xpath = "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[2]/input"
qty_field_class ="form-qty"
price_field_xpath ="/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[4]/input"
execute_btn_xpath = "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[3]/div[2]/button[1]"

odd_lot_btn_xpath = "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[1]/form/label[3]/fieldset"
mkt_order_type_btn_xpath = "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[1]/div[1]/div[2]/div[1]/label[1]/span"
