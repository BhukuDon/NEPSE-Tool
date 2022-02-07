import json
from re import search
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
