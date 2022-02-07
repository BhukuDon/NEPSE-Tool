import json
import os
#Database (python in-built)
import sqlite3
# GUI
from tkinter import *
from tkinter import font, messagebox,ttk
# GUI Icon
from PIL import Image,ImageTk

#Config File
with open ("./data/config.json","r") as read_config:
    Config=json.load(read_config)


#Fonts
font_btn = ("Arial",10)
font_lb = ("Arial",10)
