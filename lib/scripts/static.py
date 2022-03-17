import pytz
from datetime import datetime
import json
import time
import sqlite3
import sys
import os
import subprocess
import urllib.request
import glob
from pathlib import Path
import zipfile
# Get current time
def _GetTime():
    NPT = pytz.timezone('Asia/Kathmandu')
    live_time = datetime.now(NPT)

    hour = int(live_time.strftime("%H"))
    day = str(live_time.strftime("%a"))
    min = int(live_time.strftime("%M"))

    return {"hour":hour,"minute":min,"day":day}

# Log Error to error.txt
def _LogError(_filename,_lineno,_from,_error,_subheading=None):
    if _from == "clear":
        with open("./data/Error Log.txt","w") as txt_write:
            txt_write.truncate(0)
        txt_write.close()
        return
    with open("./data/Error Log.txt","a") as error_file :
        error_file.writelines(f"{_from} : ")
        if _subheading != None:
            error_file.writelines(f"{_subheading} : ")
        error_file.writelines(f"\n\tFile : {_filename}")
        error_file.writelines(f"\n\tLine no. : {_lineno}")
        time = _GetTime()
        if time["day"] == "Tue":
            time["day"] = "Tues"
        if time["day"] == "Wed":
            time["day"] = "Wednes"
        if time["day"] == "Thu":
            time["day"] = "Thurs"
        if time["day"] == "Sat":
            time["day"] = "Satur"
        error_file.writelines(f"\n\t{time['day']}day : {time['hour']}:{time['minute']}")
        error_file.writelines(f"\n\t{_error}\n")
    error_file.close()
    return

# Read/Write Config File
def _Config(_mode,_key,_value=None):
    if _mode == "r":
        with open("./data/config.json","r") as read:
            read_config = json.load(read)
        read.close()
        result = read_config[_key]
        return result
    if _mode == "w":
        with open ("./data/config.json","r") as read:
            read_config = json.load(read)
        read.close()
        read_config[_key] = _value
        with open ("./data/config.json","w") as write:
            json.dump(read_config,write,indent=4)
        write.close()
        return

def _Wait(_time,_from):
    min = _time
    hour = int(min/60)
    min = min%60

    print(_from,"Waiting =",f"{hour}:{min}")
    wait = _time*60
    time_remaining = _time
    for x in range(wait):
        if _from == "Buy":
            if _Config("r","RunningBuy") == False:
                return
        if _from == "Sell":   
            if _Config("r","RunningSell") == False:
                return
        
        wait -= 1
        if wait % 60 == 0:
            time_remaining -= 1
            min = time_remaining
            hour = int(min/60)
            min = min%60
            print(_from,"Time Remaining =",f"{hour}:{min}")

        time.sleep(1)

def _CreateDataBase():

    # Create Database if it doesn't exist
    try: 
        connection = sqlite3.connect("./data/heathens.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                nickname TEXT,
                tms_clientID INTEGER,
                tms_password TEXT,
                broker_no INTEGER
            )
        """)
        connection.commit()
        connection.close()
    except Exception as e:
        a,b,exc_tb = sys.exc_info()
        filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        _LogError(filename,exc_tb.tb_lineno,"_CreateDataBase",_error = e )
    return

class _Database :
    def __init__(self):
        pass
    def _fetchselectedprofile(self):
        if _Config("r","ProfileSelected") == False:
            return False
        oid = _Config("r","Profileoid")
        connection = sqlite3.connect("./data/heathens.db")
        cursor = connection.cursor()
        cursor.execute("SELECT *,oid FROM profile WHERE oid =:oid" ,{"oid":oid})
        data = cursor.fetchall()
        connection.close()
        return data[0]

    def _fetchallprofile(self):
        connection = sqlite3.connect("./data/heathens.db")
        cursor = connection.cursor()
        cursor.execute("SELECT *,oid FROM profile")
        data = cursor.fetchall()
        connection.close()
        if data == []:
            return False
        return data

    def _addprofile(self,nickname,client_id,password,broker_no):
        connection = sqlite3.connect("./data/heathens.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO profile VALUES (?,?,?,?)",(nickname,client_id,password,broker_no))
        connection.commit()
        connection.close()

def _CheckChrome():
    while True: # For Checking Chrome And Download If Not Avialable
        
        # Check Chrome Version
        check = 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        result = subprocess.getoutput(check)
        chrome_version = (result.split()[3])
        
        #Check if driver for that version is available
        path_extracted = './lib/drivers/{}/chromedriver.exe'.format(chrome_version)
        path_unextracted = './lib/drivers/{}/'.format(chrome_version)
        path_download = "./lib/{}.zip".format(chrome_version)
        if Path(path_extracted).is_file():
            
            _Config("w","PathToChromeDriver",path_extracted)
            break
        else:
            #Download And Unzip Driver And Set Path
            try:
                url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(chrome_version)
                urllib.request.urlretrieve(url, path_download)
            except ConnectionError as e1:
                a,b,exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                _LogError(filename,exc_tb.tb_lineno,"_CheckChrome",e1,f"Chrome Version : {chrome_version}")
                break
            except Exception as e:
                a,b,exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                _LogError(filename,exc_tb.tb_lineno,"_CheckChrome",e,f"Chrome Version : {chrome_version}")
                break
            else:
                with zipfile.ZipFile(path_download, 'r') as zip_ref:
                    zip_ref.extractall(path=path_unextracted)
                os.remove(path_download)
    return


if __name__ == "__main__":
    print("Run run.py Not static.py")
    input()
