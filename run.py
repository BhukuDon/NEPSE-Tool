
#Imports
from lib.scripts.default import *
from bot.bot import _RunBot,_Shutdown
from lib.scripts.static import _GetTime,_Config,_LogError,_Wait,_CreateDataBase,_CheckChrome,_Database
#Root Window
Root = Tk()
Root.iconbitmap("./lib/icons/logo.ico")


#Icons
if True:
    setting_icon = ImageTk.PhotoImage(Image.open("./lib/icons/settings.png").resize((28,28),Image.ANTIALIAS))         
    home_icon = ImageTk.PhotoImage(Image.open("./lib/icons/home.png").resize((25,25),Image.ANTIALIAS))         
    info_icon = ImageTk.PhotoImage(Image.open("./lib/icons/info.png").resize((20,20),Image.ANTIALIAS)) 


def _Quit(_todo = None):
    if _todo == "Buy":
        # Change RunningBuy value to False
        _Config("w","RunningBuy",False)
        _AutoBuySell("Buy")
        return
    if _todo == "Sell":
        # Change RunningSell value to False
        _Config("w","RunningSell",False)
        _AutoBuySell("Sell")
        return

    # If auto buy and sell is running ask to quit
    if _Config("r","RunningBuy") != False or _Config("r","RunningSell") != False:
        ask = messagebox.askyesnocancel("Are you sure ?","You have Auto Buy Sell Running are you sure you want to exit ?")
        if ask != True:
            return
    
    _Config("w","RunningBuy",False)
    _Config("w","RunningSell",False)
    #_Shutdown()
    quit()

class _Calc:
    # Calculation function.
    def __init__(self,buyprice=None,quantity=None,sellprice=None,capitalgain=None):
        self.buyprice = buyprice
        self.quantity = quantity
        self.sellprice = sellprice
        self.capitalgain = capitalgain
    def _buyfunc(self):
        total_price = self.buyprice * self.quantity
        if True: #Setting broker commision percentange according to total price
            if total_price <= 50000:
                broker_commision_per = 0.40
            if total_price > 50000 and total_price <= 500000 :
                broker_commision_per = 0.37
            if total_price > 500000 and total_price <= 2000000 :
                broker_commision_per = 0.34
            if total_price > 2000000 and total_price <= 10000000 :
                broker_commision_per = 0.30
            if total_price > 10000000 :
                broker_commision_per = 0.27
            broker_commision = total_price * (broker_commision_per/100)
            #If  broker commission amount is less than 10 set mininum broker commision amt
            if broker_commision < 10:
                    broker_commision = 10
        sebon_fee = total_price * (0.015/100)
        dp_charge = 25
        total_amount_payable = total_price + broker_commision + sebon_fee + dp_charge 
        cost_per_stock = total_amount_payable/self.quantity
        return([total_price,broker_commision_per,broker_commision,sebon_fee,dp_charge,total_amount_payable,cost_per_stock])
    def _sellfunc(self):
            wacc = self._buyfunc()[6]
            share_amount = self.sellprice * self.quantity
            if True: #Broker Commision
                if share_amount <= 50000:
                    broker_commision_per = 0.40
                if share_amount > 50000 and share_amount <= 500000 :
                    broker_commision_per = 0.37
                if share_amount > 500000 and share_amount <= 2000000 :
                    broker_commision_per = 0.34
                if share_amount > 2000000 and share_amount <= 10000000 :
                    broker_commision_per = 0.30
                if share_amount > 10000000 :
                    broker_commision_per = 0.27
            broker_commision = share_amount * (broker_commision_per/100)
            #If  broker commission amount is less than 10 set mininum broker commision amt
            if broker_commision < 10:
                broker_commision =  10
            sebon_fee = share_amount * (0.015/100)
            dp_charge = 25
            capital_gain = share_amount - (wacc * self.quantity)-broker_commision-sebon_fee
            capital_gain_per = float(self.capitalgain) 
            capital_gain_tax = 0
            # capital gain == profit apply tax else no tax
            if capital_gain > 0: 
                capital_gain_tax = (capital_gain)*(capital_gain_per/100)
            total_receivable = share_amount - broker_commision-sebon_fee-dp_charge-capital_gain_tax

            return[share_amount,broker_commision_per,broker_commision,sebon_fee,dp_charge,capital_gain,capital_gain_tax,total_receivable]

def _GeneralUpdate(_todo,_a=None,_b=None,_c=None):
    
    if _todo == "TermsAndCondition_checkbox":
        #Update next button

        check = _a.get()
        if check != True:
            _b.destroy() #destroy next btn
            next_btn = Button(Root, text="Next",state=DISABLED,padx=15,pady=2)
            next_btn.grid(row=3,column=3,pady=(30,0))
            return
        _b.destroy() #destroy next btn
        next_btn = Button(Root, text="Next",command=lambda:_GeneralUpdate("TermsAndCondition_btn"),padx=15,pady=2,font = ("Arial",10,"bold"))
        next_btn.grid(row=3,column=3,pady=(30,0))
        return

    if _todo == "TermsAndCondition_btn":

        # Update config 
        _Config("w","TermsAndCondition",True)
        if _Config("r","HowToUse") == False:
            _HomeScreen()
            _HowToUse()
            return
        _HomeScreen()
        return

    if _todo == "HowToUse_close" :
        check_donotshow = _a.get()
        #_b = howtouse_window

        if check_donotshow == True:
            _Config("w","HowToUse",True)
            _b.destroy()
            _HomeScreen()
            return
        _b.destroy()
        _HomeScreen()
        return

    if _todo == "HomeScreen_stocksearch":
        stock_list=_c
        combo_box = _b
        combo_box_var=_a
        value=combo_box_var.get()
        if value == '':
                combo_box['values'] = stock_list
        else:
            data = []
            for item in stock_list:
                if value.lower() in item.lower():
                    data.append(item)

            combo_box['values'] = data
            return data
        return
    
    if _todo == "HomeScreen_eventlistener":
        stock_list=_c
        combo_box = _b
        combo_box_var=_a
        data = _GeneralUpdate("HomeScreen_stocksearch",_a,_b,_c)

        try:
            combo_box.set(data[0])
        except Exception as e:
            a,b,exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _LogError(filename,exc_tb.tb_lineno,"_GeneralUpdate",e,"HomeScreen_eventlistener")
        return

    if _todo == "CreateProfile_save":
        #_a = [nickname_var,client_id_var,password_var,broker_var]
        nickname = _a[0].get()
        client_id = _a[1].get()
        password = _a[2].get()
        broker_no = _a[3].get()

        if True: #Check vars empty / int / float or not
            if nickname == "" or client_id == "" or password == "" or broker_no == "":
                messagebox.showerror("Error !","All entries but be filled.")
                return
            try: 
                nickname  = str(nickname)
            except:
                messagebox.showerror("Error !","Nickname must be a-z,A-Z,0-9.")
                return
            try: 
                client_id  = str(client_id)
            except:
                messagebox.showerror("Error !","Invalid Client ID.")
                return
            try: 
                password  = str(password)
            except:
                messagebox.showerror("Error !","Invalid Password.")
                return
            try: 
                broker_no  = int(broker_no)
            except:
                messagebox.showerror("Error !","Invalid Broker No.")
                return
            with open ("./data/broker.json","r") as read:
                brk_chk = json.load(read)
            read.close()
            if broker_no not in brk_chk:
                messagebox.showerror("Error !","Invalid Broker No.")
                return
        
        fetched_profile = _Database()._fetchallprofile()

        try:
            for profiles in fetched_profile:
                if nickname == profiles[0]:
                    messagebox.showerror("Error !",f"Already created profile with Nickname : {nickname}.")
                    return
                if client_id == profiles[1]:
                    messagebox.showerror("Error !",f"Already created profile with Client ID : {client_id}.")
                    return
        except:
            pass    
        # store data in database.
        _Database()._addprofile(nickname,client_id,password,broker_no)
        messagebox.showinfo("Success !","You have successfully create profile.")
        _CreateProfile()    

    if _todo == "CreateProfile_edit":
        #_a = [nickname_var,client_id_var,password_var,broker_var]
        nickname = _a[0].get()
        client_id = _a[1].get()
        password = _a[2].get()
        broker_no = _a[3].get()

        if True: #Check vars empty / int / float or not
            if nickname == "" or client_id == "" or password == "" or broker_no == "":
                messagebox.showerror("Error !","All entries but be filled.")
                return
            try: 
                nickname  = str(nickname)
            except:
                messagebox.showerror("Error !","Nickname must be a-z,A-Z,0-9.")
                return
            try: 
                client_id  = str(client_id)
            except:
                messagebox.showerror("Error !","Invalid Client ID.")
                return
            try: 
                password  = str(password)
            except:
                messagebox.showerror("Error !","Invalid Password.")
                return
            try: 
                broker_no  = int(broker_no)
            except:
                messagebox.showerror("Error !","Invalid Broker No.")
                return
        
        fetched_profile = _Database()._fetchallprofile()
        oid = _Database()._fetchselectedprofile()[4]
        
        for profiles in fetched_profile:
            if profiles[4] == oid:
                continue
            if nickname == profiles[0]:
                messagebox.showerror("Error !",f"Already created profile with Nickname : {nickname}.")
                return
            if client_id == profiles[1]:
                messagebox.showerror("Error !",f"Already created profile with Client ID : {client_id}.")
                return
        
        # store data in database.
        connection = sqlite3.connect("./data/heathens.db")
        cursor = connection.cursor()
        cursor.execute("""UPDATE profile SET 
            nickname=:nickname,
            tms_clientID=:client_id,
            tms_password=:password,
            broker_no=:broker_no
            Where oid =:oid""",{ "nickname":nickname,"client_id":client_id,"password":password,"broker_no":broker_no,"oid":oid})
        connection.commit()
        connection.close()
        messagebox.showinfo("Success !","You have successfully edited profile.")
        _Settings()
        return

    if _todo == "CreateProfile_delete":
        nickname = _a.get()
        conn = sqlite3.connect("./data/heathens.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profile WHERE nickname = :nickname",{"nickname":nickname})
        conn.commit()
        conn.close()
        
        _Config("w","ProfileSelected",False)
        _Config("w","Profileoid",0)

        _Settings()
        return
    
    if _todo == "Settings_selectprofile" :
        # While auto buy sell running cannot change prfile
        if _Config("r","RunningBuy") != False or _Config("r","RunningSell") != False:
            messagebox.showwarning("Warning !","You cannot change profile while Auto Buy Or Sell is running : ")
            return
        
        profile_selected  = _a.get() 
        # If profile is not created do not select any thing
        if profile_selected == "Crete Profile":
            return
        # Connecting to data base
        connection = sqlite3.connect("./data/heathens.db")
        cursor = connection.cursor()
        cursor.execute("SELECT *,oid FROM profile WHERE nickname=:nickname",{"nickname":profile_selected})
        data = cursor.fetchall()
        connection.close()

        # Dumping oid and profile is selected in config
        # Setting profile selected as true   
        _Config("w","ProfileSelected",True)
        # Getting oid
        _Config("w","Profileoid",data[0][4])
        
        _Settings()
    
    if _todo == "Settings_tesseract_path":
        # Asking for Tesseract OSR folder location
        filedir = filedialog.askdirectory(title="Select Tesseract-ORC")
        
        # If folder contians tesseract.exe dump location to config else dump fasle
        if Path(f"{filedir}/tesseract.exe").is_file():
            path = (f"{filedir}/tesseract.exe")
            _Config("w","PathToTesseract",path)
            
            return
        _Config("w","PathToTesseract",False)

        messagebox.showerror("Error !","You set Tesseract OCR folder incorrectly.")
        return
    
    if _todo == "Settings_reset" :
        response=messagebox.askyesno("Reset","This will reset the program. You will lose all data including profile and porfolio.\n Do you want to continue?")
        if response != True:
            return
            
        _Config("w","ProfileSelected",False)
        _Config("w","Profileoid",0)
        _Config("w","TermsAndCondition",False)
        _Config("w","HowToUse",False)
        _Config("w","PathToChromeDriver",False)
        _Config("w","MarketOpen",False)
        _Config("w","PathToTesseract",False)
        _Config("w","BotToken",0)
        _Config("w","RunningBot",False)
        _Config("w","ToRunBot",False)
        
        # Clearing error log
        _LogError(None,None,"clear",None)
        
        try:
            #os.remove("./data/heathens.db")
            raise Exception
        except Exception as e:
            a,b,exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _LogError(filename,exc_tb.tb_lineno,"_GeneralUpdate",e,"_Settings_reset")

            connection = sqlite3. connect("./data/heathens.db")
            cursor = connection. cursor()
            cursor. execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_name = (cursor. fetchall())
            for table in table_name[0]:
                cursor.execute(f"DROP TABLE {table}")
            connection.commit()
            connection.close()
        # remove zip file
        download_path = glob.glob("./lib/downloads/*.zip") 

        for zip in download_path:
            os.remove(zip)
        # removing driver
        
        driver_path = glob.glob("./lib/drivers/*") 
        for folder in driver_path:
            shutil.rmtree(folder)
        quit()
    return

class _class_TMS:
    def __init__(self,order_type=None,stock=None,quantity=None,price=None,driver=None):
        self.order_type = order_type
        self.stock = stock
        self.quantity = quantity
        self.price = price
        fetch_profile_details = _Database()._fetchselectedprofile()
        self.driver = driver

        self.nickname = fetch_profile_details[0]
        self.clientid = fetch_profile_details[1]
        self.password = fetch_profile_details[2]
        self.brokerno = fetch_profile_details[3]

    def _marketstatus(self):


        # Fetching nepali time and day
        time = _GetTime()
        hour = time["hour"]
        day = time["day"]
        min = time["minute"]
        
        market_open_days = ["Sun","Mon","Tue","Wed","Thu"]
        week = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

        # If today is not market open day
        if day not in market_open_days:
            # if config running is true change it to false
            if _Config("r","MarketOpen") != False:
                _Config("w","MarketOpen",False)
            # check if tommorow is in market open day or not    
            tom_day = week.index(day)
            
            day_to_skip = -1
            time_to_sleep = 0
            while tom_day not in market_open_days:
            #exception will occur if tommorow is sunday 
                try: 
                    tom_day = week[tom_day+1]
                    day_to_skip += 1
                except:
                    tom_day = "Sun"
                    day_to_skip += 1
            
                time_to_sleep = ((24-hour)+11)*60 # mins till 12 am + hours till market open time
                time_to_sleep = time_to_sleep - min # mins to wait minus current min
                time_to_sleep = time_to_sleep + (day_to_skip*24*60) # mins to wait + days to skip
            return [False,time_to_sleep] # in minutes
        
        #If Time is not between 11 - 3 even if its market open day
        if hour < 10 or hour > 14: 
            if _Config("r","MarketOpen") != False:
                _Config("w","MarketOpen",False)
            

            time_to_sleep = (24 - hour + 11)*60
            time_to_sleep -= min

            return [False,time_to_sleep]
    
    
        # if market already checked once between 11 -- 3
        if _Config("r","MarketOpen") == True:
            return [True,0]
        
        # if market not checked till now or checked but returned Closed
        try:
            market_status = requests.get("http://www.nepalstock.com/" ,headers=Nepalstock_Header).text
            soup = BeautifulSoup(market_status, 'lxml')
            temp = soup.find('div', id= 'top-notice-bar').text
            fetch = temp[8:]
            fetch =fetch[:5]
            if fetch == "Close":

                if _Config("r","MarketOpen") != False:
                    _Config("w","MarketOpen",False)
                
                return [False,60] # wait 1 hour
            
            _Config("w","MarketOpen",True)
            return [True,0]       
        except Exception as e:
            a,b,exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_marketstatus")
            
            try:
                driver = webdriver.Chrome(_Config("r","PathToChromeDriver"))
                driver.get("https://nepsealpha.com/trading/chart")
                iframe = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/iframe'))
                )

            except Exception as e: 
                a,b,exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_marketstatus")
                driver.close()
                return ["Error",5]# wait 5 mins



            driver.switch_to.frame(iframe)
            driver.implicitly_wait(60)            
            status = driver.find_element(By.XPATH,market_status_xpath)

            if status.get_attribute("innerText")[:11] == "MARKET OPEN":
                _Config("w","MarketOpen",True)

                return [True,0]
            if status.get_attribute("innerText")[:11] != "MARKET OPEN":
                if _Config("r","MarketOpen") != False:
                    _Config("w","MarketOpen",False)
                    
                return [False,60]# wait one hour
            
        return
    
    def _scrapeltp(self):

        url = "https://nepsealpha.com/trading/1/quotes?symbols={}".format(self.stock)
        # Request LTP from nepsealpha
        try:
            fetch = requests.get(url,headers=Nepsealpha_Header)

        except Exception as e:
            a,b,exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_scrapeltp")
            
            return False
        else:
            fetched_data = json.loads(fetch.content)
            ltp = fetched_data["d"][0]["v"]["lp"]
            open_price = fetched_data["d"][0]["v"]["open_price"]
            return [float(ltp),float(open_price)]

    def _insertclientid(self):

        if self.brokerno < 10:
            self.brokerno = "0"+str(self.brokerno)
        url = "https://tms{}.nepsetms.com.np/".format(self.brokerno)
        self.driver.get(url)
        
         
        while True:

            try:
                client_code = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, client_code_field_xpath))
                )

            except Exception as e: 
                a,b,exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_insertclientid")
                self.driver.refresh()
                time.sleep(60)
                continue
            else:
                client_code.send_keys(self.clientid)
                return True

    def _insertpassword(self):
        while True:
            self.driver.find_element(By.CLASS_NAME,'captcha-image-dimension').screenshot('./lib/captcha.png')
            image = cv2.imread("./lib/captcha.png")
            
            image = cv2.fastNlMeansDenoisingColored(image,None,8,10,5,21)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            pytesseract.pytesseract.tesseract_cmd= _Config("r","PathToTesseract")
            
            captcha = pytesseract.image_to_string(image)
            
            password = self.driver.find_element(By.ID,password_field_id)
            password.send_keys(self.password)
            captcha_field = self.driver.find_element(By.ID,captcha_field_id)
            captcha_field.send_keys(captcha[:6])
            login_btn= self.driver.find_element(By.XPATH,login_btn_xpath)
            time.sleep(3)
            login_btn.click()
            # Checking if error box appears or not
            try:
                check = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "toast-text"))
                )
                x = check.get_attribute("innerText")
            except TimeoutException: 
                return True
            except Exception as e:
                a,b,exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_insertpassword")
                continue
            else:
                if x[:14] == "Wrong Captcha!":
                    continue
                messagebox.showerror("Error !","TMS ID/Password is incorrect. Or make sure you have entered the correct broker no.")
                return False

    def _move(self):
        while True:
            try:
                dropdown_a = self.driver.find_element(By.XPATH,dropdown_xpath)
                dropdown_a.click()

                buysell_a = self.driver.find_element(By.XPATH,buysell_hyperlink_xpath)
                buysell_a.click()
            except Exception as e:
                a,b,exc_tb = sys.exc_info()
                filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_move")
                self.driver.refresh()
                time.sleep(10)
                continue
            else: 
                try:
                    check = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, toogle_sell_xpath))
                    )

                except Exception as e:
                    a,b,exc_tb = sys.exc_info()
                    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    _LogError(filename,exc_tb.tb_lineno,"_class_TMS",e,"_move")
                    self.driver.refresh()
                    time.sleep(10)
                    continue
                else: 
                    return True

    def _buy(self):
    
        toogle_buy = self.driver.find_element(By.XPATH,toogle_buy_xpath)
        toogle_buy.click()
        time.sleep(1)


        if self.quantity < 10:
            odd_lot = self.driver.find_element(By.XPATH,odd_lot_btn_xpath)
            odd_lot.click()

        script_field = self.driver.find_element(By.XPATH,script_field_xpath)
        script_field.send_keys(self.stock)
        time.sleep(1)
        
        qty_field = self.driver.find_element(By.CLASS_NAME,qty_field_class)
        qty_field.send_keys(self.quantity)

        if self.order_type == "MKT":
            mkt_lot = self.driver.find_element(By.XPATH,mkt_order_type_btn_xpath)
            mkt_lot.click()
        if self.order_type != "MKT":

            price_field = self.driver.find_element(By.XPATH,price_field_xpath)
            price_field.send_keys(self.price)

        action_button= self.driver.find_element(By.XPATH,execute_btn_xpath)   

        action_button.click()
        time.sleep(100)
        self.driver.quit()
        
        _Config("w","RunningBuy",False)

        _AutoBuySell("Buy")
        return

    def _sell(self):
    
        toogle_sell = self.driver.find_element(By.XPATH,toogle_sell_xpath)
        toogle_sell.click()
        time.sleep(1)


        if self.quantity < 10:
            odd_lot = self.driver.find_element(By.XPATH,odd_lot_btn_xpath)
            odd_lot.click()

        script_field = self.driver.find_element(By.XPATH,script_field_xpath)
        script_field.send_keys(self.stock)
        time.sleep(1)
        
        qty_field = self.driver.find_element(By.CLASS_NAME,qty_field_class)
        qty_field.send_keys(self.quantity)

        if self.order_type == "MKT":
            mkt_lot = self.driver.find_element(By.XPATH,mkt_order_type_btn_xpath)
            mkt_lot.click()
        if self.order_type != "MKT":

            price_field = self.driver.find_element(By.XPATH,price_field_xpath)
            price_field.send_keys(self.price)

        action_button= self.driver.find_element(By.XPATH,execute_btn_xpath)   

        action_button.click()
        time.sleep(100)
        self.driver.quit()
        
        _Config("w","RunningSell",False)
        _AutoBuySell("Sell")
        return

def _UpdateFrame(_mode,data):
    # Return funtion if running is false:
    if _mode == "Buy":
        if _Config("r","RunningBuy") == False:
            return
    if _mode == "Sell":
        if _Config("r","RunningSell") == False:
            return
    
    # Continue if title doesn't say autobuysell window is open
    if Root.title() != "AutoBuySell | Tool":
        return
    frame_list = []
    mode = ""
    # fetch frame if title says autobuysell window is open
    for frame in Root.winfo_children():
        frame_list.append(frame)
    
    # fetch buy/sell button to see if which mode we are in i.e buy or sell
    for widgets in frame_list[0].winfo_children():
        if (widgets.config()["text"][4]) == "Buy":
            if (widgets.config()["state"][4]) != "normal":
                mode = "Buy"
                break
            mode = "Sell"
    
    # if we are not in the mode we need to configure continue
    if _mode != mode:
        return
    
    # else
    all_visiible_widgets = []
    for widgets in frame_list[1].winfo_children():
        all_visiible_widgets.append(widgets)
    label = (all_visiible_widgets[len(all_visiible_widgets)-3])
    
    label.config(text=data)

    label.config(background="#f8fad7")
    
    
    if data[:3] == "LTP":
        label.config(background="#5f948f")

    if data[:5] == "Error":
        label.config(background="#bb4a54")

    if data[:7] == "Success":
        label.config(background="#afd68d")

    time_var = 30
            
def _TMS(_todo,_info_list):
    #list = [order_type,stock,quantity,price/stoploss,target]

    quantity = _info_list[2]
    stock = _info_list[1]
    order_type = _info_list[0]
    time_sleep = 0

    while True:
        if _todo == "Buy":
            if _Config("r","RunningBuy") == False:
                return
        if _todo == "Sell":
            if _Config("r","RunningSell") == False:
                return
        _Wait(time_sleep,_todo)

        # Checking Market open or not
        open_or_not = _class_TMS()._marketstatus()

        # If market closed
        if open_or_not[0] == False:
            time_sleep = open_or_not[1]

            _Config("w",f"MarketData{_todo}","Market Closed")
            threading.Thread(target = lambda:_UpdateFrame(_todo,"Market Closed")).start()
            continue
        if open_or_not[0] == "Error":
            # Sleep for 1 min
            time_sleep = open_or_not[1]
            _Config("w",f"MarketData{_todo}","Error ! Trying again.")
            threading.Thread(target = lambda:_UpdateFrame(_todo,"Error ! Trying again.")).start()

            continue
        
        # Fetch LTP
        ltp_fetch = _class_TMS(stock=stock)._scrapeltp()

        # If LTP fetched error
        if ltp_fetch == False:
            
            _Config("w",f"MarketData{_todo}","Error ! Trying again.")
            threading.Thread(target = lambda:_UpdateFrame(_todo,"Error ! Trying again.")).start()
            time_sleep = 5 # 5 mins 
            continue
        ltp = ltp_fetch[0]
        open_price = ltp_fetch[1]

        _Config("w",f"MarketData{_todo}",f"LTP : {ltp}")
        threading.Thread(target = lambda:_UpdateFrame(_todo,f"LTP : {ltp}")).start() 
        # Buying Stock
        if _todo == "Buy": 
            if _Config("r","RunningBuy") == False:
                return
            #list = [order_type,stock,quantity,price]
            buy_price = _info_list[3]

            near_buyprice_1 = buy_price + (open_price*0.01)
            near_buyprice_2 = buy_price + (open_price*0.02)

            #If ltp is less or equal to buy price
            if ltp <= buy_price:
                # buy if price start increasing again 
                low_ltp = ltp
                time_var_low = 1
                while True:
                    if _Config("r","RunningBuy") == False:
                        return
                    _Wait(time_var_low,_todo)
                    market_status_low = _class_TMS()._marketstatus()

                    #if market Closed
                    if market_status_low[0] == False:

                        _Config("w",f"MarketData{_todo}","Market Closed")
                        threading.Thread(target = lambda:_UpdateFrame(_todo,"Market Closed")).start() 

                        break
                    #if market fetch error
                    if market_status_low[0] != "Error":
                        time_var_low = 1 #1 minute


                        _Config("w",f"MarketData{_todo}","Error ! Trying again.")
                        threading.Thread(target = lambda:_UpdateFrame(_todo,"Error ! Trying again.")).start() 
                        continue
                    
                    ltp_open_scrape_low = _class_TMS(stock=stock)._scrapeltp()
                    if ltp_open_scrape_low == False:
                        time_var_low = 1 # 1 minute

                        _Config("w",f"MarketData{_todo}","Error ! Trying again.")
                        threading.Thread(target = lambda:_UpdateFrame(_todo,"Error ! Trying Again")).start() 
                        continue

                    _Config("w",f"MarketData{_todo}",f"LTP : {ltp_open_scrape_low[0]}")
                    threading.Thread(target = lambda:_UpdateFrame(_todo,f"LTP : {ltp_open_scrape_low[0]}")).start()

                    # If ltp is less than low price Update
                    if ltp_open_scrape_low[0] < low_ltp:
                        low_ltp = ltp_open_scrape_low[0]
                    # If ltp is more than low price buy
                    if ltp_open_scrape_low[0] > low_ltp:
                        driver = webdriver.Chrome(_Config("r","PathToChromeDriver"))
                        _class_TMS(driver=driver)._insertclientid()

                        if _class_TMS(driver=driver)._insertpassword() != False:
                            _class_TMS(driver=driver)._move()
                            _class_TMS(driver=driver,stock = stock,quantity = quantity,order_type="MKT")._buy()
                        return
                    time_var_low = 0.5 # half a minute
                continue
            # if ltp is near buying price decreasing time 
            if ltp <= near_buyprice_1:
                time_sleep = 1 # 1 min
                continue
            if ltp <= near_buyprice_2:
                time_sleep = 2 #2 mins
                continue
            time_sleep = 3 # 3mins    
            continue
        
        # Selling Stock
        if _todo == "Sell":
            if _Config("r","RunningSell") == False:
                return
            
            #list = [order_type,stock,quantity,stoploss,target]
            
            stoploss = _info_list[3]
            target = _info_list[4]
            quantity = _info_list[2]

            near_stoploss_1 = stoploss + (open_price*0.01)
            near_stoploss_2 = stoploss + (open_price*0.02)
            
            near_target_1 = target + (open_price*0.01)
            near_target_2 = target + (open_price*0.02)

            if ltp <= stoploss:
                _class_TMS(driver=driver)._insertclientid()
                if _class_TMS(driver=driver)._insertpassword() != False:
                    _class_TMS(driver=driver)._move()
                    if order_type != "LMT":
                        _class_TMS(driver=driver,stock = stock,quantity = quantity,order_type=order_type)._sell()
                        return
                    _class_TMS(driver=driver,stock = stock,quantity = quantity,order_type=order_type,price=stoploss)._sell()
                return
            # if ltp is greater than target
            if ltp >= target:
                time_var_high = 0
                high_ltp = ltp
                while True:
                    if _Config("r","RunningSell") == False:
                        return
                    _Wait(time_var_high,_todo)
                    market_status_high = _class_TMS()._marketstatus()

                    #if market Close
                    if market_status_high == False:
                        break
                    #if market fetch error
                    if market_status_high != False and market_status_high != True:
                        time_var_high = 1 # 1 min
                        continue
                    
                    nepse_alpha_fetched_high = _class_TMS(stock=stock)._scrapeltp()
                    #if nepse fetch error
                    if nepse_alpha_fetched_high == False:
                        time_var_high = 1 # 1 min
                        continue
                    # if ltp is greater than high ltp Update
                    if nepse_alpha_fetched_high[0] > high_ltp:
                        high_ltp = nepse_alpha_fetched_high[0]
                    # if ltp is lesser than high ltp Sell
                    if nepse_alpha_fetched_high[0] < high_ltp:
                        driver = webdriver.Chrome(_Config("r","PathToChromeDriver"))
                        _class_TMS(driver=driver)._insertclientid()
                        
                        if _class_TMS(driver=driver)._insertpassword() != False:
                            _class_TMS(driver=driver)._move()
                            _class_TMS(driver=driver,stock=stock,quantity=quantity,order_type="MKT")._sell()
                        return
                    
                    time_var_high = 0.5 # 30 sec
                continue

            # If ltp is near stop loss or target
            if ltp <= near_stoploss_1 or ltp <= near_target_1 :
                time_sleep = 1 # 1 min
                continue
            if ltp <= near_stoploss_2 or ltp <= near_target_2 :
                time_sleep = 2 # 2 min
                continue

            time_sleep = 3 # 3 mins
            continue

        return

def _ValidateStock(text):
    with open("./data/stock.json","r") as read_temp:
        read_stock = json.load(read_temp)
    read_temp.close()  
    
    stock = text
    if text[0] == "(":
        temp = text[1:].split(")")
        stock = temp[0]
    # if stock not present in stock.json fetch if stock is valid or not in nepsealpha.
    if stock not in read_stock:
        url = "https://nepsealpha.com/trading/1/symbols?symbol={}".format(stock)
        try:
            fetch = requests.get(url,headers=Nepsealpha_Header)
        except ConnectionError:
            return "Error"
        if fetch.status_code == 404 :
            return False
        #else append stock to stock.json
        data = json.loads(fetch.content)

        read_stock[stock] =  [data["description"],data["type"]]
        with open ("./data/stock.json","w") as write_temp :
            json.dump(read_stock,write_temp,indent=4)
        write_temp.close()
    return True

def _ValidateAutoBuySell(_todo,_var_list):
    
    quantity = _var_list[2].get()
    stock = _var_list[1].get()
    order_type = _var_list[0].get()
    stock = stock.upper()
    # checking var list is int/float/string and stock symbol is valid also all the feild is empty or not
    if quantity == "" or stock == "":
        messagebox.showerror("Error !","Feild Empty. Please fill in all the details.")
        return

    try :
            quantity = int(quantity)
    except : 
        messagebox.showerror("Error !","Quantity must be number (Integer).")
        return
    
    temp = _ValidateStock(stock)

    if temp == False:
            messagebox.showerror("Error !","Stock doesn't exist. Please enter valid stock.")
            return
    if temp == "Error":
            messagebox.showerror("Error !","Please check you connection. Connection Error.")
            return

    if _todo == "Buy":
        #var_list = [order_type_var,stock_var,quantity_var,stoploss,target]
        
        
        price = _var_list[3].get()
        # checking var list is int/float/string and stock symbol is valid also all the feild is empty or not
        if price == "" :
            messagebox.showerror("Error !","Feild Empty. Please fill in all the details.")
            return
       
        try :
            price = float(price)
        except : 
            messagebox.showerror("Error !","Price must be number (Integer/Float).")
        

        if stock[0] == "(":
            temp = stock[1:].split(")")
            stock = temp[0]
        list = [order_type,stock,quantity,price]

        # Set running buy value true
        
        _Config("w","MarketDataBuy","Running")
        _Config("w","RunningBuy",list)
        _AutoBuySell("Buy")
        
        threading.Thread(target = lambda:_TMS(_todo,list)).start()
        return

    if _todo == "Sell":
        #var_list = [order_type_var,stock_var,quantity_var,stoploss,target]
        stoploss = _var_list[3].get()
        target = _var_list[4].get()
        if stoploss == "" or target == "":
            messagebox.showerror("Error !","Feild Empty. Please fill in all the details.")
            return
       
        try :
            stoploss = float(stoploss)
        except : 
            messagebox.showerror("Error !","Stoploss must be number (Integer/Float).")
            return
       
        try :
            target = float(target)
        except : 
            messagebox.showerror("Error !","Target must be number (Integer/Float).")
            return
        
        # target must be greater than stop loss
        if target <= stoploss:
            messagebox.showerror("Error !","Target must be greater than Stoploss.")
            return 

        list = [order_type,stock,quantity,stoploss,target]
        
        #var_list = [order_type_var,stock_var,quantity_var,stoploss,target]
        _Config("w","MarketDataSell","Running")
        _Config("w","RunningSell",list)
        _AutoBuySell("Sell")
        threading.Thread(target = lambda:_TMS(_todo,list)).start()
        return
    return

def _AutoBuySell(_menu):
    #Root title,size
    Root.title("AutoBuySell | Tool")
    Root.geometry("600x300")
    #If any delete all the previous widgets from window
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass
        
    #Setting MarketOpen to its default value False
    _Config("w","MarketOpen",False)


    # Seting Frames 
    menu_frame = Frame(Root)
    input_frame = Frame(Root)
    running_frame = Frame(Root,background="#90ee90",width=600,relief=SUNKEN)
    running_frame.grid(row=1,column=1,sticky = W + E)
    menu_frame.grid(row=2,column=1)
    input_frame.grid(row=3,column=1,pady=(35,0))
    
    #Disable everything and send messagebox if profile not selected
    if _Config("r","ProfileSelected") == False or _Config("r","PathToTesseract") == False or _Config("r","PathToChromeDriver") == False:

        buy_btn = Button(menu_frame,text = "Buy",state= DISABLED,padx=13,pady=3,font=font_btn)
        sell_btn = Button(menu_frame,text = "Sell",state= DISABLED,padx=13,pady=3,font=font_btn)
        profile_lb = Label(menu_frame,text = "Profile : #######",font = font_lb)
        home_btn = Button(menu_frame,image = home_icon,command=_HomeScreen)
        buy_btn.grid(row=1,column=1,padx=(30,0),pady=(25,0))
        sell_btn.grid(row=1,column=2,padx=(20,0),pady=(25,0))
        profile_lb.grid(row=1,column=3,padx=(95,0),pady=(25,0))
        home_btn.grid(row=1,column=4,padx=(195,0),pady=(25,0))

        order_type_var = StringVar()
        order_type_list = ["LMT","MKT"]
        order_type_var.set(order_type_list[0])
        order_type_lb = Label(input_frame,text = "Order Type : ",font = font_lb)
        order_type_opt = OptionMenu(input_frame,order_type_var,*order_type_list)
        order_type_info = Button(input_frame,image = info_icon,command=lambda:messagebox.showinfo("Order Type Info","Please watch this video if you want info on order type: https://www.youtube.com/watch?v=jbE7dl3wof8 "))
        order_type_lb.grid(row=1,column=1,padx=(0,40))
        order_type_opt.grid(row=1,column=2)
        order_type_info.grid(row=1,column=3,padx=(25,0))

        stock_var = StringVar()
        stock_lb = Label(input_frame,text= "Stock : ",font = font_lb)
        stock_etr = Entry(input_frame,width = 20, textvariable= stock_var,state= DISABLED)
        stock_lb.grid(row=2,column=1,padx=(0,68),pady=(10,0))
        stock_etr.grid(row=2,column=2,pady=(10,0))

        quantity_var = StringVar()
        quantity_lb = Label(input_frame,text="Quantity : ",font=font_lb)
        quantity_etr = Entry(input_frame,width=20,textvariable=quantity_var,state= DISABLED)
        quantity_lb.grid(row=3,column=1,padx=(0,55),pady=(10,0))
        quantity_etr.grid(row=3,column=2,pady=(10,0))
        
        price_var = StringVar()
        price_lb =  Label(input_frame,text= "Price To Buy Below : ",font=font_lb)
        price_etr = Entry(input_frame,width=20,textvariable=price_var,state= DISABLED)
        price_info = Button(input_frame,image=info_icon,command=lambda:messagebox.showinfo("Price Info","Please enter the price you want to buy below."))
        price_lb.grid(row=4,column=1,padx=(0,43),pady=(10,0))
        price_etr.grid(row=4,column=2,pady=(10,0))
        price_info.grid(row=4,column=3,padx=(25,0),pady=(10,0))

        var_list = [order_type_var,stock_var,quantity_var,price_var]

        buy_btn  = Button(input_frame,text="Buy",state= DISABLED,padx=13,pady=3,font=font_btn)
        buy_btn.grid(row=5,column=1,columnspan=2,pady=(20,0))

        
        # Showing warning
        if _Config("r","ProfileSelected") == False:
            messagebox.showwarning("Warning !","You cannot use this feature unless you setup your profile.'\n To setup your profile please go to Settings > Create Profile and seleted your profile in settings.")
        if _Config("r","PathToTesseract") == False:
            messagebox.showwarning("Warning !","You cannot use this feature unless you install Tesseract OCR and set its folder in Settings.'\n To go to https://github.com/UB-Mannheim/tesseract/wiki and install it. Or you can also install it with the setup i have provided in setup folder.")
        if _Config("r","PathToChromeDriver") == False:
            messagebox.showwarning("Warning !","Chrome Driver not found either you haven't installed Chrome or the driver didn't download correctly.")
        return

    profile_text = _Database()._fetchselectedprofile()[0]
    profile_text = f"Profile : {profile_text}"

    with open("./data/stock.json","r") as stock_read:
        stock_list_temp = json.load(stock_read)
    stock_read.close()
    stock_list = []
    for data in stock_list_temp:
        stock_list.append(f"({data}) {stock_list_temp[data][0]}")

    if _menu == "Buy":

        if True: # Declaring Wigdets
            buy_btn = Button(menu_frame,text = "Buy",state= DISABLED,padx=13,pady=3,font=font_btn)
            sell_btn = Button(menu_frame,text = "Sell",command=lambda:_AutoBuySell("Sell"),padx=13,pady=3,font=font_btn)
            profile_lb = Label(menu_frame,text = profile_text,font = font_lb)
            home_btn = Button(menu_frame,image = home_icon,command=_HomeScreen)
            buy_btn.grid(row=1,column=1,padx=(30,0),pady=(25,0))
            sell_btn.grid(row=1,column=2,padx=(20,0),pady=(25,0))
            profile_lb.grid(row=1,column=3,padx=(95,0),pady=(25,0))
            home_btn.grid(row=1,column=4,padx=(195,0),pady=(25,0))

            order_type_var = StringVar()
            order_type_list = ["LMT","MKT"]
            order_type_var.set(order_type_list[0])
            order_type_lb = Label(input_frame,text = "Order Type : ",font = font_lb)
            order_type_opt = OptionMenu(input_frame,order_type_var,*order_type_list)
            order_type_info = Button(input_frame,image = info_icon,command=lambda:messagebox.showinfo("Order Type Info","Please watch this video if you want info on order type: https://www.youtube.com/watch?v=jbE7dl3wof8 "))
            order_type_lb.grid(row=1,column=1,padx=(0,40))
            order_type_opt.grid(row=1,column=2)
            order_type_info.grid(row=1,column=3,padx=(25,0))

            stock_var = StringVar()
            stock_lb = Label(input_frame,text= "Stock : ",font = font_lb)
            search_script_ety = ttk.Combobox(input_frame,value=stock_list)
            search_script_ety.config(width=18,height=3,textvariable=stock_var)
            search_script_ety.bind("<KeyRelease>",lambda e: _GeneralUpdate("HomeScreen_stocksearch",stock_var,search_script_ety,stock_list))
            search_script_ety.bind("<Return>",lambda e: _GeneralUpdate("HomeScreen_eventlistener",stock_var,search_script_ety,stock_list))
            stock_lb.grid(row=2,column=1,padx=(0,68),pady=(10,0))
            search_script_ety.grid(row=2,column=2,pady=(10,0))



            quantity_var = StringVar()
            quantity_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_etr = Entry(input_frame,width=20,textvariable=quantity_var)
            quantity_lb.grid(row=3,column=1,padx=(0,55),pady=(10,0))
            quantity_etr.grid(row=3,column=2,pady=(10,0))
            
            price_var = StringVar()
            price_lb =  Label(input_frame,text= "Buy Below : ",font=font_lb)
            price_etr = Entry(input_frame,width=20,textvariable=price_var)
            price_info = Button(input_frame,image=info_icon,command=lambda:messagebox.showinfo("Price Info","Please enter the price you want to buy below."))
            price_lb.grid(row=4,column=1,padx=(0,43),pady=(10,0))
            price_etr.grid(row=4,column=2,pady=(10,0))
            price_info.grid(row=4,column=3,padx=(25,0),pady=(10,0))

            current_data = Label(input_frame,text="",font=font_lb,padx=10,pady=2,relief=SUNKEN)
            var_list = [order_type_var,stock_var,quantity_var,price_var]
        
        if _Config("r","RunningBuy") != False:
            buy_btn  = Button(input_frame,text="Buy",state = DISABLED,font=font_btn,padx=13,pady=3)
            buy_btn.grid(row=6,column=1,pady=(20,0))

            quit_btn  = Button(input_frame,text="Quit",command = lambda: _Quit("Buy"),font=font_btn,padx=13,pady=3)
            quit_btn.grid(row=6,column=2,pady=(20,0))

            Root.geometry("600x350")

            running_order_type_lb = Label(running_frame,text = "Order Type : {}".format(_Config("r","RunningBuy")[0]),font = font_lb,background = "#90ee90")
            running_stock_lb = Label(running_frame,text = "Stock : {}".format(_Config("r","RunningBuy")[1]),font = font_lb,background = "#90ee90")
            running_quantity_lb = Label(running_frame,text = "Quantity : {}".format(_Config("r","RunningBuy")[2]),font = font_lb,background = "#90ee90")
            running_price_lb = Label(running_frame,text = "Buy Below : {}".format(_Config("r","RunningBuy")[3]),font = font_lb,background = "#90ee90")
            running_order_type_lb.grid(row=1,column=1,pady=10,padx=(55,0))
            running_stock_lb.grid(row=1,column=2,pady=10,padx=(40,0))
            running_quantity_lb.grid(row=1,column=3,pady=10,padx=(40,0))
            running_price_lb.grid(row=1,column=4,pady=10,padx=(40,60))

            data = _Config("r","MarketDataBuy")
            if data != False:
                current_data.config(text=data)
                current_data.grid(row=5,column=1,columnspan=2,pady=(20,0))

                current_data.config(background="#0000FF")
                Root.geometry("600x380")

                if data[:5] == "Error":
                    current_data.config(background="#FF0000")
                if data[:7] == "Success":
                    current_data.config(background="#00FF00")
            return
        buy_btn  = Button(input_frame,text="Buy",command=lambda: _ValidateAutoBuySell("Buy",var_list),font=font_btn,padx=13,pady=3)
        buy_btn.grid(row=6,column=1,columnspan=2,pady=(20,0))
        return

    if _menu == "Sell":
        if True: # Declaring Wigdets
            buy_btn = Button(menu_frame,text = "Buy",command=lambda:_AutoBuySell("Buy"),padx=13,pady=3,font=font_btn)
            sell_btn = Button(menu_frame,text = "Sell",state= DISABLED,padx=13,pady=3,font=font_btn)
            profile_lb = Label(menu_frame,text = profile_text,font = font_lb)
            home_btn = Button(menu_frame,image = home_icon,command=_HomeScreen)
            buy_btn.grid(row=1,column=1,padx=(30,0),pady=(25,0))
            sell_btn.grid(row=1,column=2,padx=(20,0),pady=(25,0))
            profile_lb.grid(row=1,column=3,padx=(95,0),pady=(25,0))
            home_btn.grid(row=1,column=4,padx=(195,0),pady=(25,0))

            order_type_var = StringVar()
            order_type_list = ["LMT","MKT"]
            order_type_var.set(order_type_list[0])
            order_type_lb = Label(input_frame,text = "Order Type : ",font = font_lb)
            order_type_opt = OptionMenu(input_frame,order_type_var,*order_type_list)
            order_type_info = Button(input_frame,image = info_icon,command=lambda:messagebox.showinfo("Order Type Info","Please watch this video if you want info on order type: https://www.youtube.com/watch?v=jbE7dl3wof8 "))
            order_type_lb.grid(row=1,column=1,padx=(0,60))
            order_type_opt.grid(row=1,column=2)
            order_type_info.grid(row=1,column=3,padx=(25,0))

            stock_var = StringVar()
            stock_lb = Label(input_frame,text= "Stock : ",font = font_lb)
            search_script_ety = ttk.Combobox(input_frame,value=stock_list)
            search_script_ety.config(width=18,height=3,textvariable=stock_var)
            search_script_ety.bind("<KeyRelease>",lambda e: _GeneralUpdate("HomeScreen_stocksearch",stock_var,search_script_ety,stock_list))
            search_script_ety.bind("<Return>",lambda e: _GeneralUpdate("HomeScreen_eventlistener",stock_var,search_script_ety,stock_list))
            stock_lb.grid(row=2,column=1,padx=(0,90),pady=(7,0))
            search_script_ety.grid(row=2,column=2,pady=(7,0))

            quantity_var = StringVar()
            quantity_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_etr = Entry(input_frame,width=20,textvariable=quantity_var)
            quantity_lb.grid(row=3,column=1,padx=(0,73),pady=(7,0))
            quantity_etr.grid(row=3,column=2,pady=(7,0))
            
            stoploss_var = StringVar()
            stoploss_lb = Label(input_frame,text="Stoploss : ",font=font_lb)
            stoploss_etr = Entry(input_frame,width=20,textvariable=stoploss_var)
            stoploss_lb.grid(row=4,column=1,padx=(0,73),pady=(7,0))
            stoploss_etr.grid(row=4,column=2,pady=(7,0))
            
            target_var = StringVar()
            target_lb = Label(input_frame,text="Target : ",font=font_lb)
            target_etr = Entry(input_frame,width=20,textvariable=target_var)
            target_lb.grid(row=5,column=1,padx=(0,85),pady=(7,0))
            target_etr.grid(row=5,column=2,pady=(7,0))

            current_data = Label(input_frame,text="",font=font_lb,padx=10,pady=2,relief=SUNKEN)

            var_list = [order_type_var,stock_var,quantity_var,stoploss_var,target_var]

        if _Config("r","RunningSell") != False:
            sell_btn  = Button(input_frame,text="Sell",state=DISABLED,padx=13,pady=3,font=font_btn)
            sell_btn.grid(row=7,column=1,pady=(15,0))

            quit_btn  = Button(input_frame,text="Quit",command = lambda: _Quit("Sell"),font=font_btn,padx=13,pady=3)
            quit_btn.grid(row=7,column=2,pady=(15,0))

            Root.geometry("600x350")

            running_order_type_lb = Label(running_frame,text = "Order Type : {}".format(_Config("r","RunningSell")[0]),font = font_lb,background = "#90ee90")
            running_stock_lb = Label(running_frame,text = "Stock : {}".format(_Config("r","RunningSell")[1]),font = font_lb,background = "#90ee90")
            running_quantity_lb = Label(running_frame,text = "Quantity : {}".format(_Config("r","RunningSell")[2]),font = font_lb,background = "#90ee90")
            running_stoploss_lb = Label(running_frame,text = "Stoploss : {}".format(_Config("r","RunningSell")[3]),font = font_lb,background = "#90ee90")
            running_target_lb = Label(running_frame,text = "Target : {}".format(_Config("r","RunningSell")[4]),font = font_lb,background = "#90ee90")
            running_order_type_lb.grid(row=1,column=1,pady=10,padx=(40,0))
            running_stock_lb.grid(row=1,column=2,pady=10,padx=(20,0))
            running_quantity_lb.grid(row=1,column=3,pady=10,padx=(20,0))
            running_stoploss_lb.grid(row=1,column=4,pady=10,padx=(20,0))
            running_target_lb.grid(row=1,column=5,pady=10,padx=(20,40))

            data = _Config("r","MarketDataSell")
            if data != False:
                Root.geometry("600x380")

                current_data.config(text=data)
                current_data.grid(row=6,column=1,columnspan=2,pady=(20,0))

                current_data.config(background="#0000FF")

                if data[:5] == "Error":
                    current_data.config(background="#FF0000")
                if data[:7] == "Success":
                    current_data.config(background="#00FF00")
            return
        sell_btn  = Button(input_frame,text="Sell",command=lambda: _ValidateAutoBuySell("Sell",var_list),padx=13,pady=3,font=font_btn)
        sell_btn.grid(row=7,column=1,columnspan=2,pady=(15,0))
        return

    return

def _CalculatorUpdate(_todo,_frame,_a=None,_b=None,_c=None,_d=None,_e=None,_f=None,_g=None):
    if _todo == "Buy":
        buy_price = _a.get()
        quantity = _b.get()
        #Changing to int/float 
        try :
            buy_price=float(buy_price)
            quantity=int(quantity)
        # set value = 0  to show result as "*"
        except:
            buy_price=0
            quantity=0
        
        if buy_price==0 or quantity == 0:
            #Forgeting and then re-assigning result labels as "*".
            _c[0].config(text="*")
            _c[1].config(text='Broker Commision (*) : ')
            _c[2].config(text="*")
            _c[3].config(text="*")    
            _c[4].config(text="*")
            _c[5].config(text="*")
            _c[6].config(text="*")
            return  
        
        if True: # if both buy&quantity is not zero
            #Forgeting and then re-assigning result labels as respectative answers.
            ans = _Calc(buy_price,quantity)._buyfunc()
            _c[0].config(text="{:.2f}".format(ans[0]))
            _c[1].config(text='Broker Commision ({}) : '.format(ans[1]))
            _c[2].config(text="{:.2f}".format(ans[2]))
            _c[3].config(text="{:.2f}".format(ans[3]))    
            _c[4].config(text="{:.2f}".format(ans[4]))
            _c[5].config(text="{:.2f}".format(ans[5]))
            _c[6].config(text="{:.2f}".format(ans[6]))
   
    if _todo == "Sell":
        #"Sell",result__frame,buy_price_var,sell_price_var,quantity_var,capital_gain_tax_var,forget_list
        buy_price = _a.get()
        sell_price = _b.get()
        quantity = _c.get()
        capital_gain_tax= _d.get()

        # Converting to float/int if not empty

        try :
            buy_price =float(buy_price)
            sell_price = float(sell_price)
            quantity = int(quantity)
        # Exception = set value 0 to show result as "*"
        except:
            buy_price =0
            sell_price = 0
            quantity = 0

        if buy_price == 0 or sell_price == 0 or quantity == 0 :
            # Destroying and re-assigning label as "*"
            _e[0].config(text="*")
            _e[1].config(text="Broker Commision (*) : ")
            _e[2].config(text="*")
            _e[3].config(text="*")
            _e[4].config(text="*")
            _e[5].config(text="*")
            _e[6].config(text="*")
            _e[7].config(text="*")
            
            # try to destroy profit or loss label if declared
            for temp in _frame.winfo_children():
                try:
                    if temp.grid_info()["row"] == 8:
                        temp.destroy()
                except:
                    pass
            return
        #if buy/sell/quantity is not 0
        if True:
            ans = _Calc(buy_price,quantity,sell_price,capital_gain_tax)._sellfunc()
            
            _e[0].config(text="{:.2f}".format(ans[0]))
            _e[1].config(text=f"Broker Commision ({ans[1]}) : ")
            _e[2].config(text="{:.2f}".format(ans[2]))
            _e[3].config(text="{:.2f}".format(ans[3]))
            _e[4].config(text="{:.2f}".format(ans[4]))
            _e[5].config(text="{:.2f}".format(ans[5]))
            _e[6].config(text="{:.2f}".format(ans[6]))
            _e[7].config(text="{:.2f}".format(ans[7]))
            
            # try to destroy profit or loss label if declared
            for temp in _frame.winfo_children():
                try:
                    if temp.grid_info()["row"] == 8:
                        temp.destroy()
                except:
                    pass 
            if ans[5] > 0:
                profit_label = Label(_frame, text = "Profit : ",font=font_lb)
                profit_label.grid(row=8,column=1,pady=(5,0),padx=(0,90))
                
            if ans[5] < 0:
                loss_label = Label(_frame, text = "Loss : ",font=font_lb)
                loss_label.grid(row=8,column=1,pady=(5,0),padx=(0,100))
            profit_value = Label(_frame, text = "{:.2f}".format(ans[5]-ans[6]-ans[4]))
            profit_value.grid(row=8,column=2,pady=(5,0),padx=(20,0))

    if _todo == "Average":
        # Assigning parameter
        if True: 
            try:
                buy_var_1 = _a.get()
                quantity_var_1 = _b.get()
                buy_var_2 = _c.get()
                quantity_var_2 = _d.get()
            except:
                pass
            rest_var = _e
            result_frame = _g

        
        # Fetching visible grids/non visible inputs / visible inputs / result list
        if True:

            visible_grid = [] # grid that are visible
            non_visible_widgets = [] # non visible widgets i.e (label/entries)
            visible_widgets = [] # visible widgets i.e (label/entries)
            visible_entries = [] # visible entries)
            for input_widgets in _frame.winfo_children():
                temp = str(input_widgets).split(".!")
                if temp[2][:5] == "entry":
                    try:
                        (input_widgets.grid_info()["row"])
                    except:
                        pass
                    else:
                        visible_entries.append(input_widgets)

                try:
                    visible_grid.append(input_widgets.grid_info()["row"])
                except:
                    non_visible_widgets.append(input_widgets)
                else:
                    visible_widgets.append(input_widgets)
            for double in visible_grid:
                if visible_grid.count(double) > 1 :
                    visible_grid.remove(double)
            for double in visible_grid:
                if visible_grid.count(double) > 1 :
                    visible_grid.remove(double)
                                 
            result_list =[] # Result label
            try: # Try if result is visible 
                for labels in result_frame.winfo_children():
                    temp = str(labels).split(".!")
                    if temp[2][:5] == "label":
                        result_list.append(labels)
            except:
                pass
        #Adding new buys
        if _f == "Add":
                            
            if visible_grid[len(visible_grid)-1] == 20:
                messagebox.showerror("Error !","Max add limit i.e. 10 reached.\n You cannot add more than 10 inputs") 
                return
            to_add_grid = (visible_grid[len(visible_grid)-1])
            non_visible_widgets[0].grid(row=to_add_grid+1,column=1,columnspan=4,pady=(10,0))
            non_visible_widgets[1].grid(row=to_add_grid+2,column=1,pady=(5,0))
            non_visible_widgets[2].grid(row=to_add_grid+2,column=2,pady=(5,0))
            non_visible_widgets[3].grid(row=to_add_grid+2,column=3,pady=(5,0))
            non_visible_widgets[4].grid(row=to_add_grid+2,column=4,pady=(5,0))

            Root.geometry(f"600x{(Root.winfo_height())+60}")
            return
        #Deleting last buy
        if _f == "Delete":

            
            if visible_grid[len(visible_grid)-1] == 4:
                messagebox.showerror("Error !","Max delete limit i.e. 2 reached.\n You cannot delete more than 2 inputs") 
                return
            visible_widgets[len(visible_widgets)-1].grid_forget()
            visible_widgets[len(visible_widgets)-2].grid_forget()
            visible_widgets[len(visible_widgets)-3].grid_forget()
            visible_widgets[len(visible_widgets)-4].grid_forget()
            visible_widgets[len(visible_widgets)-5].grid_forget()
            Root.geometry(f"600x{(Root.winfo_height())-60}")
            return
        
        
        try: #Checking all variables is float/ int or not
            start = 0
            end = len(visible_entries)-1
            buy_var_1 =float(buy_var_1)
            quantity_var_1=int(quantity_var_1)
            buy_var_2=float(buy_var_2)
            quantity_var_2=int(quantity_var_2)

            buy_list = []
            quantity_list = []
            if len(visible_entries) != 4:
                for num in range(start,end-3,2):
                    x=rest_var[num].get()
                    
                    buy_list.append(float(x))
        
        
                for num in range(start+1,end-2,2):
                    x=rest_var[num].get()

                    quantity_list.append(int(x))
        except Exception as e:
            buy_var_1 = 0
            quantity_var_1 = 0
            buy_var_2 = 0
            quantity_var_2 = 0

        
        #If any of the variable is not int/float or empty
        if buy_var_1 == 0 or quantity_var_1 == 0 or buy_var_2 == 0 or quantity_var_2 == 0: 
            result_list[1].destroy()
            result_list[1] = Label(result_frame,text="*")
            result_list[1].grid(row=2,column=2,pady=(20,0))
            return
        
        #Getting wacc rate for all
        wacc1 = _Calc(buy_var_1,quantity_var_1)._buyfunc()[5]
        wacc2 = _Calc(buy_var_2,quantity_var_2)._buyfunc()[5]
        rest_wacc =[]
        try:
            for num in range(int(len(visible_entries)/2)):
                wacc = _Calc(buy_list[num],quantity_list[num])._buyfunc()[5]
                rest_wacc.append(wacc)
        except :
            pass
        
        #getting total price and total quantity 
        total_price_list = [wacc1,wacc2]
        for wacc in rest_wacc:
            total_price_list.append(wacc)
        total_price=0
        for wacc in total_price_list:
            total_price=total_price+wacc
        total_quantity = quantity_var_1+quantity_var_2
        for quantity in quantity_list:
            total_quantity=total_quantity+quantity
        #showing result
        result_list[1].destroy()
        result_list[1] = Label(result_frame,text="{:.2f}".format(total_price/total_quantity))
        result_list[1].grid(row=2,column=2,pady=(20,0))
        
    return

def _Calculator(_menu):
    #Root title,size
    Root.title("Calculator | Tool")
    Root.geometry("600x300")
    #If any delete all the previous widgets from window
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass
    
    menu_frame = Frame(Root)
    menu_frame.grid(row=1,column=1)
    if _menu == "Buy":
        if True: # Menu Widgets
            buy_menu_btn = Button(menu_frame,text="Buy",state=DISABLED,padx=7,pady=1,font=font_btn)
            sell_menu_btn = Button(menu_frame,text="Sell",command=lambda:_Calculator("Sell"),padx=7,pady=2,font=font_btn)
            average_menu_btn = Button(menu_frame,text="Average",command=lambda:_Calculator("Average"),padx=7,pady=2,font=font_btn)
            home_btn = Button(menu_frame,image=home_icon,padx=3,pady=3,command=_HomeScreen)
            buy_menu_btn.grid(row=1,column=1,pady=(20,0),padx=(40,0))
            sell_menu_btn.grid(row=1,column=2,pady=(20,0),padx=(40,0))
            average_menu_btn.grid(row=1,column=3,pady=(20,0),padx=(40,0))
            home_btn.grid(row=1,column=4,pady=(20,0),padx=(260,20))
        if True: # Frame Widgets
            input_frame = Frame(Root)
            input_frame.grid(row=2,column=1)
            buy_price_var= StringVar()
            quantity_var= StringVar()        
            buy_price_lb = Label(input_frame,text="Buying Price : " ,font=font_lb)
            buy_price_etr = Entry(input_frame,width=20,textvariable=buy_price_var)
            buy_price_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Buy",result_frame,buy_price_var,quantity_var,forget_list))
            quantity_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_etr = Entry(input_frame,width=20,textvariable=quantity_var)
            quantity_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Buy",result_frame,buy_price_var,quantity_var,forget_list))
            buy_price_lb.grid(row=2,column=1,pady=(20,0),padx=(0,0))
            buy_price_etr.grid(row=2,column=2,pady=(20,0),padx=(20,0))
            quantity_lb.grid(row=2,column=3,pady=(20,0),padx=(20,0))
            quantity_etr.grid(row=2,column=4,pady=(20,0),padx=(20,0))
        if True: # Result Widgets
            result_frame = Frame(Root)
            result_frame.grid(row=3,column=1)

            total_price_lb = Label(result_frame,text='Total Price : ',font=font_lb)
            total_price_input = Label(result_frame,text='*')
            total_price_lb.grid(row=1,column=1,padx=(0,63),pady=(25,0))        
            total_price_input.grid(row=1,column=2,pady=(25,0))        


            broker_commision_lb = Label(result_frame,text='Broker Commision (*) : ',font=font_lb)
            broker_commision_input = Label(result_frame,text='*')
            broker_commision_lb.grid(row=2,column=1,padx=(0,0),pady=(5,0))        
            broker_commision_input.grid(row=2,column=2,pady=(5,0))        
            
            sebon_fee_lb = Label(result_frame,text='SEBON Fee : ',font=font_lb)
            sebon_fee_input = Label(result_frame,text='*')
            sebon_fee_lb.grid(row=3,column=1,padx=(0,53),pady=(5,0))        
            sebon_fee_input.grid(row=3,column=2,pady=(5,0))        

            dp_charge_lb = Label(result_frame,text='DP Charge : ',font=font_lb)
            dp_charge_input = Label(result_frame,text='*')
            dp_charge_lb.grid(row=4,column=1,padx=(0,60),pady=(5,0))        
            dp_charge_input.grid(row=4,column=2,pady=(5,0))        

            total_payable_amt_lb = Label(result_frame,text='Total Amount Payable : ',font=font_lb)
            total_payable_amt_input = Label(result_frame,text='*')
            total_payable_amt_lb.grid(row=5,column=1,padx=(0,0),pady=(5,0))        
            total_payable_amt_input.grid(row=5,column=2,pady=(5,0))        

            cost_per_stock_lb = Label(result_frame,text='Cost Per Stock : ',font=font_lb)
            cost_per_stock_input = Label(result_frame,text='*')
            cost_per_stock_lb.grid(row=6,column=1,padx=(0,38),pady=(5,0))        
            cost_per_stock_input.grid(row=6,column=2,pady=(5,0))        
            
        forget_list = [total_price_input,broker_commision_lb,broker_commision_input,sebon_fee_input,dp_charge_input,total_payable_amt_input,cost_per_stock_input]
            
    if _menu == "Sell":
        Root.geometry("600x400")

        if True: # Menu Widgets

            buy_menu_btn = Button(menu_frame,text="Buy",command=lambda:_Calculator("Buy"),padx=7,pady=1,font=font_btn)
            sell_menu_btn = Button(menu_frame,text="Sell",state=DISABLED,padx=7,pady=2,font=font_btn)
            average_menu_btn = Button(menu_frame,text="Average",command=lambda:_Calculator("Average"),padx=7,pady=2,font=font_btn)
            home_btn = Button(menu_frame,image=home_icon,padx=3,pady=3,command=_HomeScreen)
            buy_menu_btn.grid(row=1,column=1,pady=(20,0),padx=(40,0))
            sell_menu_btn.grid(row=1,column=2,pady=(20,0),padx=(40,0))
            average_menu_btn.grid(row=1,column=3,pady=(20,0),padx=(40,0))
            home_btn.grid(row=1,column=4,pady=(20,0),padx=(260,20))

        if True: # Input Widgets
            input_frame = Frame(Root)
            input_frame.grid(row=2,column=1)

            buy_price_var = StringVar()
            sell_price_var = StringVar()
            quantity_var = StringVar()
            capitalgainlist = [7.5,5]
            capital_gain_tax_var = DoubleVar()

            buy_price_lb = Label(input_frame, text="Buying Price : ",font=font_lb)
            buy_price_etr = Entry(input_frame, width=20, textvariable=buy_price_var)
            buy_price_etr.bind("<KeyRelease>",lambda e : _CalculatorUpdate("Sell",result_frame,buy_price_var,sell_price_var,quantity_var,capital_gain_tax_var,forget_list))
            sell_price_lb = Label(input_frame, text="Selling Price : ",font=font_lb)
            sell_price_etr = Entry(input_frame,width = 20,textvariable=sell_price_var)
            sell_price_etr.bind("<KeyRelease>",lambda e : _CalculatorUpdate("Sell",result_frame,buy_price_var,sell_price_var,quantity_var,capital_gain_tax_var,forget_list))
            buy_price_lb.grid(row=1,column=1,pady=(40,0),padx=(0,5))
            buy_price_etr.grid(row=1,column=2,pady=(40,0),padx=(0,0))
            sell_price_lb.grid(row=1,column=3,pady=(40,0),padx=(0,0))
            sell_price_etr.grid(row=1,column=4,pady=(40,0),padx=(0,0))
            

            capital_gain_tax_var.set(capitalgainlist[0])
            quantity_lb = Label(input_frame,text="Quality : ",font=font_lb)
            quantity_etr = Entry(input_frame,text="Quality : ",textvariable=quantity_var)
            quantity_etr.bind("<KeyRelease>",lambda e : _CalculatorUpdate("Sell",result_frame,buy_price_var,sell_price_var,quantity_var,capital_gain_tax_var,forget_list))
            capital_gain_tax_lb = Label(input_frame,text="Capital Gain Tax : ",font=font_lb)
            capital_gain_tax_opt = OptionMenu(input_frame,capital_gain_tax_var,*capitalgainlist)
            capital_gain_tax_var.trace("w",lambda e,f,g: _CalculatorUpdate("Sell",result_frame,buy_price_var,sell_price_var,quantity_var,capital_gain_tax_var,forget_list))
            quantity_lb.grid(row=2,column=1,pady=(10,0),padx=(0,35))
            quantity_etr.grid(row=2,column=2,pady=(10,0),padx=(0,0))
            capital_gain_tax_lb.grid(row=2,column=3,pady=(10,0),padx=(20,0))
            capital_gain_tax_opt.grid(row=2,column=4,pady=(10,0),padx=(0,0))
        
        if True: # Result Widgets
            result_frame = Frame(Root)
            result_frame.grid(row=3,column=1)
            
            share_amount_lb = Label(result_frame,text="Share Amount : ",font=font_lb)
            share_amount_input = Label(result_frame,text="*")
            share_amount_lb.grid(row=1,column=1,pady=(20,0),padx=(0,50))
            share_amount_input.grid(row=1,column=2,pady=(20,0),padx=(20,0))

            broker_commision_lb = Label(result_frame,text="Broker Commision (*) : " ,font=font_lb)
            broker_commision_input = Label(result_frame,text="*")
            broker_commision_lb.grid(row=2,column=1,pady=(5,0),padx=(0,10))
            broker_commision_input.grid(row=2,column=2,pady=(5,0),padx=(20,0))

            sebon_fee_lb = Label(result_frame,text= "SEBON Fee : ",font=font_lb)
            sebon_fee_input = Label(result_frame,text="*")
            sebon_fee_lb.grid(row=3,column=1,pady=(5,0),padx=(0,65))
            sebon_fee_input.grid(row=3,column=2,pady=(5,0),padx=(20,0))

            dp_fee_lb = Label(result_frame,text="DP Fee : ",font=font_lb)
            dp_fee_input= Label(result_frame,text="*")
            dp_fee_lb.grid(row=4,column=1,pady=(5,0),padx=(0,90))
            dp_fee_input.grid(row=4,column=2,pady=(5,0),padx=(20,0))

            capital_gain_lb = Label(result_frame,text= "Capital Gain : ",font=font_lb)
            capital_gain_input = Label(result_frame,text="*")
            capital_gain_lb.grid(row=5,column=1,pady=(5,0),padx=(0,70))
            capital_gain_input.grid(row=5,column=2,pady=(5,0),padx=(20,0))

            capital_gain_tax_lb = Label(result_frame, text="Capital Gain Tax : ",font=font_lb)
            capital_gain_tax_input = Label(result_frame,text="*")
            capital_gain_tax_lb.grid(row=6,column=1,pady=(5,0),padx=(0,45))
            capital_gain_tax_input.grid(row=6,column=2,pady=(5,0),padx=(20,0))

            total_receivable_lb = Label(result_frame,text= "Total Receivable Amount : ",font=font_lb)
            total_receivable_input=  Label(result_frame,text="*")
            total_receivable_lb.grid(row=7,column=1,pady=(5,0),padx=(0,0))
            total_receivable_input.grid(row=7,column=2,pady=(5,0),padx=(20,0))

        forget_list =[share_amount_input,broker_commision_lb,broker_commision_input,sebon_fee_input,dp_fee_input,capital_gain_input,capital_gain_tax_input,total_receivable_input]

    if _menu == "Average":
        Root.geometry("600x280")
        if True: # Menu Widgets

            buy_menu_btn = Button(menu_frame,text="Buy",command=lambda:_Calculator("Buy"),padx=7,pady=1,font=font_btn)
            sell_menu_btn = Button(menu_frame,text="Sell",command=lambda:_Calculator("Sell"),padx=7,pady=2,font=font_btn)
            average_menu_btn = Button(menu_frame,text="Average",state=DISABLED,padx=7,pady=2,font=font_btn)
            home_btn = Button(menu_frame,image=home_icon,padx=3,pady=3,command=_HomeScreen)
            buy_menu_btn.grid(row=1,column=1,pady=(20,0),padx=(40,0))
            sell_menu_btn.grid(row=1,column=2,pady=(20,0),padx=(40,0))
            average_menu_btn.grid(row=1,column=3,pady=(20,0),padx=(40,0))
            home_btn.grid(row=1,column=4,pady=(20,0),padx=(260,20))

        if True: # Input Widgets
            
            input_frame = Frame(Root)
            input_frame.grid(row=2,column=1)
            result_frame = Frame(Root)
            result_frame.grid(row=3,column=1,pady=(20,0))
            
            buy_price_1_var = StringVar()
            quantity_1_var = StringVar()
            buy_price_2_var = StringVar()
            quantity_2_var = StringVar()
            buy_price_3_var = StringVar()
            quantity_3_var = StringVar()
            buy_price_4_var = StringVar()
            quantity_4_var = StringVar()
            buy_price_5_var = StringVar()
            quantity_5_var = StringVar()
            buy_price_6_var = StringVar()
            quantity_6_var = StringVar()
            buy_price_7_var = StringVar()
            quantity_7_var = StringVar()
            buy_price_8_var = StringVar()
            quantity_8_var = StringVar()
            buy_price_9_var = StringVar()
            quantity_9_var = StringVar()
            buy_price_10_var = StringVar()
            quantity_10_var = StringVar()
            rest_var = [buy_price_3_var,quantity_3_var,buy_price_4_var,quantity_4_var,buy_price_5_var,quantity_5_var,buy_price_6_var,quantity_6_var,buy_price_7_var,quantity_7_var,buy_price_8_var,quantity_8_var,buy_price_9_var,quantity_9_var,buy_price_10_var,quantity_10_var]

            buy_price_1_title = Label(input_frame, text="1st Buy",font=font_lb)
            buy_price_1_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_1_etr = Entry(input_frame,width=20, textvariable=buy_price_1_var)
            buy_price_1_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_1_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_1_etr = Entry(input_frame,width=20,textvariable=quantity_1_var)
            quantity_1_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            buy_price_1_title.grid(row=1,column=1,columnspan=4,pady=(20,0))
            buy_price_1_lb.grid(row=2,column=1,pady=(5,0))
            buy_price_1_etr.grid(row=2,column=2,pady=(5,0))
            quantity_1_lb.grid(row=2,column=3,pady=(5,0))
            quantity_1_etr.grid(row=2,column=4,pady=(5,0))

            buy_price_2_title = Label(input_frame, text="2nd Buy",font=font_lb)
            buy_price_2_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_2_etr = Entry(input_frame,width=20, textvariable=buy_price_2_var)
            buy_price_2_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_2_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_2_etr = Entry(input_frame,width=20,textvariable=quantity_2_var)
            quantity_2_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            buy_price_2_title.grid(row=3,column=1,columnspan=4,pady=(10,0))
            buy_price_2_lb.grid(row=4,column=1,pady=(5,0))
            buy_price_2_etr.grid(row=4,column=2,pady=(5,0))
            quantity_2_lb.grid(row=4,column=3,pady=(5,0))
            quantity_2_etr.grid(row=4,column=4,pady=(5,0))

            buy_price_3_title = Label(input_frame, text="3rd Buy",font=font_lb)
            buy_price_3_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_3_etr = Entry(input_frame,width=20, textvariable=buy_price_3_var)
            buy_price_3_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_3_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_3_etr = Entry(input_frame,width=20,textvariable=quantity_3_var)
            quantity_3_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_4_title = Label(input_frame, text="4th Buy",font=font_lb)
            buy_price_4_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_4_etr = Entry(input_frame,width=20, textvariable=buy_price_4_var)
            buy_price_4_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_4_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_4_etr = Entry(input_frame,width=20,textvariable=quantity_4_var)
            quantity_4_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_5_title = Label(input_frame, text="5th Buy",font=font_lb)
            buy_price_5_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_5_etr = Entry(input_frame,width=20, textvariable=buy_price_5_var)
            buy_price_5_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_5_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_5_etr = Entry(input_frame,width=20,textvariable=quantity_5_var)
            quantity_5_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_6_title = Label(input_frame, text="6th Buy",font=font_lb)
            buy_price_6_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_6_etr = Entry(input_frame,width=20, textvariable=buy_price_6_var)
            buy_price_6_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_6_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_6_etr = Entry(input_frame,width=20,textvariable=quantity_6_var)
            quantity_6_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_7_title = Label(input_frame, text="7th Buy",font=font_lb)
            buy_price_7_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_7_etr = Entry(input_frame,width=20, textvariable=buy_price_7_var)
            buy_price_7_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_7_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_7_etr = Entry(input_frame,width=20,textvariable=quantity_7_var)
            quantity_7_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_8_title = Label(input_frame, text="8th Buy",font=font_lb)
            buy_price_8_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_8_etr = Entry(input_frame,width=20, textvariable=buy_price_8_var)
            buy_price_8_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_8_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_8_etr = Entry(input_frame,width=20,textvariable=quantity_8_var)
            quantity_8_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_9_title = Label(input_frame, text="9th Buy",font=font_lb)
            buy_price_9_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_9_etr = Entry(input_frame,width=20, textvariable=buy_price_9_var)
            buy_price_9_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_9_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_9_etr = Entry(input_frame,width=20,textvariable=quantity_9_var)
            quantity_9_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

            buy_price_10_title = Label(input_frame, text="10th Buy",font=font_lb)
            buy_price_10_lb= Label(input_frame, text="Buy Price : ",font=font_lb)
            buy_price_10_etr = Entry(input_frame,width=20, textvariable=buy_price_10_var)
            buy_price_10_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))
            quantity_10_lb = Label(input_frame,text="Quantity : ",font=font_lb)
            quantity_10_etr = Entry(input_frame,width=20,textvariable=quantity_10_var)
            quantity_10_etr.bind("<KeyRelease>",lambda e:_CalculatorUpdate("Average",input_frame,buy_price_1_var,quantity_1_var,buy_price_2_var,quantity_2_var,rest_var,_g=result_frame))

        if True: # Result Widgets


            add_btn = Button(result_frame,text = "Add",command= lambda: _CalculatorUpdate("Average",input_frame,_f="Add"))
            delete_btn = Button(result_frame,text = "Delete", command= lambda: _CalculatorUpdate("Average",input_frame,_f="Delete"))
            result_lb = Label(result_frame,text = "Average Cost Per Stock : ",font=font_lb)
            result_input = Label(result_frame,text="*")
            add_btn.grid(row=1,column=1)
            delete_btn.grid(row=1,column=2)
            result_lb.grid(row=2,column=1,pady=(20,0))
            result_input.grid(row=2,column=2,pady=(20,0))

    return

def _CreateProfile():
    Root.title("Create Profile | Tool")
    Root.geometry("600x300")
    # Clearing all widgets
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass

    back_btn = Button(Root,text="Back",font=font_btn,padx=13,pady=3,command=_Settings)
    back_btn.grid(row=1,column=3,pady=(25,0),padx=(240,0))

    nickname_var = StringVar()
    nickname_lb = Label(Root,text="Nickname : ",font=font_lb)
    nickname_etr = Entry(Root,width=20,textvariable=nickname_var)
    nickname_lb.grid(row=2,column=1,pady=(20,0),padx=(15,0))
    nickname_etr.grid(row=2,column=2,pady=(20,0))

    client_id_var = StringVar()
    client_id_lb = Label(Root,text="TMS Client ID : ",font=font_lb)
    client_id_etr = Entry(Root,width=20,textvariable=client_id_var)
    client_id_lb.grid(row=3,column=1,pady=(10,0),padx=(35,0))
    client_id_etr.grid(row=3,column=2,pady=(10,0))

    password_var = StringVar()
    password_lb = Label(Root,text="TMS Password : ",font=font_lb)
    password_etr = Entry(Root,width=20,textvariable=password_var)
    password_lb.grid(row=4,column=1,pady=(10,0),padx=(40,0))
    password_etr.grid(row=4,column=2,pady=(10,0))

    broker_var = StringVar()
    broker_lb = Label(Root,text="Broker No. : ",font=font_lb)
    broker_etr = Entry(Root,width=20,textvariable=broker_var)
    broker_lb.grid(row=5,column=1,pady=(10,0),padx=(20,0))
    broker_etr.grid(row=5,column=2,pady=(10,0))

    var =[nickname_var,client_id_var,password_var,broker_var]
    save_btn = Button(Root,text="Save",font=font_btn,padx=13,pady=3,command = lambda:_GeneralUpdate("CreateProfile_save",var))
    save_btn.grid(row=6,column=3,pady=(50,0),padx=(240,0))
    return

def _ShowProfile():

    # Clearing all widgets
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass

    fetch_selected_profile = _Database()._fetchselectedprofile()
    nickname = fetch_selected_profile[0]
    client_id = fetch_selected_profile[1]
    password = fetch_selected_profile[2]
    broker_no = fetch_selected_profile[3]
    
    Root.title(f"{nickname} Profile | Tool")
    Root.geometry("600x300")

    back_btn = Button(Root,text="Back",font=font_btn,padx=13,pady=3,command=_Settings)
    back_btn.grid(row=1,column=3,pady=(25,0),padx=(240,0))

    nickname_var = StringVar()
    nickname_lb = Label(Root,text="Nickname : ",font=font_lb)
    nickname_etr = Entry(Root,width=20,textvariable=nickname_var)
    nickname_etr.insert(END,nickname)
    nickname_lb.grid(row=2,column=1,pady=(20,0),padx=(15,0))
    nickname_etr.grid(row=2,column=2,pady=(20,0))

    client_id_var = StringVar()
    client_id_lb = Label(Root,text="TMS Client ID : ",font=font_lb)
    client_id_etr = Entry(Root,width=20,textvariable=client_id_var)
    client_id_etr.insert(END,client_id)
    client_id_lb.grid(row=3,column=1,pady=(10,0),padx=(35,0))
    client_id_etr.grid(row=3,column=2,pady=(10,0))

    password_var = StringVar()
    password_lb = Label(Root,text="TMS Password : ",font=font_lb)
    password_etr = Entry(Root,width=20,textvariable=password_var)
    password_etr.insert(END,password)
    password_lb.grid(row=4,column=1,pady=(10,0),padx=(40,0))
    password_etr.grid(row=4,column=2,pady=(10,0))

    broker_var = StringVar()
    broker_lb = Label(Root,text="Broker No. : ",font=font_lb)
    broker_etr = Entry(Root,width=20,textvariable=broker_var)
    broker_etr.insert(END,broker_no)
    broker_lb.grid(row=5,column=1,pady=(10,0),padx=(20,0))
    broker_etr.grid(row=5,column=2,pady=(10,0))

    var =[nickname_var,client_id_var,password_var,broker_var]
    
    del_btn = Button(Root,text = "Delete",font=font_btn,padx=13,pady=3,command = lambda:_GeneralUpdate("CreateProfile_delete",nickname_var))
    del_btn.grid(row=6,column=1,pady=(50,0),padx=(40,0))
    save_btn = Button(Root,text="Save",font=font_btn,padx=13,pady=3,command = lambda:_GeneralUpdate("CreateProfile_edit",var))
    save_btn.grid(row=6,column=3,pady=(50,0),padx=(240,0))
    return

def _Settings():
    Root.title("Settings | Tool")
    Root.geometry("600x300")
    # Clearing all widgets 
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass

    # home button
    profile_var = StringVar()
    profile_list = []
    fetched_profile = _Database()._fetchallprofile()

    if _Config("r","ProfileSelected") == False:

        if fetched_profile == False:
            profile_list = ["Crete Profile"]
            profile_var.set("Crete Profile")
        else:
            fetched_profile = _Database()._fetchallprofile()
            for profiles in fetched_profile:
                profile_list.append(profiles[0])
            profile_var.set("Select A Profile")

    if _Config("r","ProfileSelected") == True:
            fetched_profile = _Database()._fetchallprofile()
            fetched_selected_profile = _Database()._fetchselectedprofile()
            for profiles in fetched_profile:
                profile_list.append(profiles[0])
            profile_var.set(fetched_selected_profile[0])
    home_btn = Button(Root,image=home_icon,command=_HomeScreen) 
    home_btn.grid(row=1,column=3,pady=(25,0),padx=(270,10))

    create_profile_btn = Button(Root,text="Create Profile",font=font_btn,padx=13,pady=3,command = _CreateProfile)
    create_profile_btn.grid(row=2,column=1,columnspan=2,pady=(20,0))

    # command update selected profile
    select_profile_lb = Label(Root,text="Select Profile : ",font=font_lb)
    select_profile_opt = OptionMenu(Root,profile_var,*profile_list,command=lambda e:_GeneralUpdate("Settings_selectprofile",profile_var))
    select_profile_opt.config(height=1,width=15)
    select_profile_lb.grid(row=3,column=1,pady=(20,0),padx=(40,0))
    select_profile_opt.grid(row=3,column=2,pady=(20,0))
    if _Config("r","ProfileSelected") == True:
        show_profile_details_btn = Button(Root,text="Show Profile Details",font=font_btn,padx=13,pady=3,command=_ShowProfile)
    else:
        show_profile_details_btn = Button(Root,text="Show Profile Details",font=font_btn,padx=13,pady=3,command=lambda:messagebox.showerror("Error !","Please select a profile first."))
    show_profile_details_btn.grid(row=4,column=1,columnspan=2,pady=(20,0),padx=(0,0))
    
    info_msg = """
You'll need to install Tesseract-OCR engine in order to use Auto Buy & Sell feature.
Please go to https://github.com/UB-Mannheim/tesseract/wiki and install it. 
Or you can also install it with the setup i have provided in setup folder.
After installing set its folder by click on Tesseract-OCR Button.
    """

    tesseract_path_btn = Button(Root,text="Tesseract-OCR",font=font_btn,padx=13,pady=3,command=lambda:_GeneralUpdate("Settings_tesseract_path"))
    tesseract_path_info = Button(Root, image = info_icon,command = lambda: messagebox.showinfo("Tesseract-OCR",info_msg))
    tesseract_path_btn.grid(row=5,column=1,padx=(10,0),pady=(0,0))
    tesseract_path_info.grid(row=5,column=2)

    reset_btn = Button(Root,text="Reset",font=("Arial",10,"bold"),padx=13,pady=3,command=lambda:_GeneralUpdate("Settings_reset"))
    reset_btn.grid(row=5,column=3,pady=(35,0),padx=(230,10))
    
    return

def _HomeScreen():
    #Root title,size
    Root.title("Home | Tool")
    Root.geometry("600x300")
    #If any delete all the previous widgets from window
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass
    
    calculator_btn = Button(Root,text="Calculator",font=font_btn,padx=13,pady=3,command=lambda:_Calculator("Buy"))
    setting_btn = Button(Root,image=setting_icon,command= _Settings)
    calculator_btn.grid(row=1,column=1,padx=(15,0),pady=(25,0))
    setting_btn.grid(row=1,column=5,pady=(25,0),padx=(0,15))

    search_script_info_para="""
Use this feature to search any stock listed on NEPSE.
This shows basic information about the stock.
    """
    
    #Make This Dynamic


    with open("./data/stock.json","r") as stock_read:
        stock_list_temp = json.load(stock_read)
    stock_read.close()
    stock_list = []
    for data in stock_list_temp:
        stock_list.append(f"({data}) {stock_list_temp[data][0]}")

    search_script_var = StringVar()
    search_script_lb = Label(Root,text="Search Stock : ",font=font_lb)
    search_script_ety = ttk.Combobox(Root,value=stock_list)
    search_script_ety.config(width=30,height=3,textvariable=search_script_var)
    search_script_ety.bind("<KeyRelease>",lambda e: _GeneralUpdate("HomeScreen_stocksearch",search_script_var,search_script_ety,stock_list))
    search_script_ety.bind("<Return>",lambda e: _GeneralUpdate("HomeScreen_eventlistener",search_script_var,search_script_ety,stock_list))
    search_script_btn = Button(Root,text="Search",padx=13,pady=3,font=font_btn)
    search_script_info = Button(Root,image=info_icon,command= lambda: messagebox.showinfo("Search Stock Feature",search_script_info_para))
    search_script_lb.grid(row=2,column=1,padx=(14,0),pady=(25,0))
    search_script_ety.grid(row=2,column=2,padx=(5,0),pady=(25,0))
    search_script_btn.grid(row=2,column=3,padx=(20,0),pady=(25,0))
    search_script_info.grid(row=2,column=4,padx=(15,0),pady=(25,0))

    # Sector selected Var and list
    
    show_all_sector_stock_info_para="""
Use this feature to search every stock from selected sector listed on NEPSE.
This shows basic information about the stock.
    """
    sector_list = ["Com. Bank","Dev. Bank","Finance","Hydro","Hotel"]
    sector_var = StringVar()
    sector_var.set("Select a sector")
    show_all_sector_stock_lb = Label(Root, text="Show Sector Stocks : ",font=font_lb)
    show_all_sector_stock_opt= OptionMenu(Root,sector_var,*sector_list)
    show_all_sector_stock_opt.config(width=13,height=1)
    show_all_sector_stock_btn = Button(Root,text="Search",padx=13,pady=3,font=font_btn)
    show_all_sector_stock_info = Button(Root,image=info_icon,command=lambda: messagebox.showinfo("Show Sector Stocks Feature",show_all_sector_stock_info_para))
    show_all_sector_stock_lb.grid(row=3,column=1,padx=(50,0),pady=(20,0))
    show_all_sector_stock_opt.grid(row=3,column=2,pady=(20,0))
    show_all_sector_stock_btn.grid(row=3,column=3,padx=(20,0),pady=(20,0))
    show_all_sector_stock_info.grid(row=3,column=4,padx=(15,0),pady=(20,0))

    autobuysell_info_para = """
This feature is used for buying or selling any stock automatically. 
The program must be running to execute buy or sell so please do not close the program.
After executing the given instruction it will automatically update porfolio if any of the profile you have selected.
    """

    portfolio_btn = Button(Root,text="Portfolio",padx=13,pady=3,font=font_btn)
    auto_buy_sell_btn = Button(Root,text="Auto Buy & Sell",padx=13,pady=3,font=font_btn,command=lambda:_AutoBuySell("Buy"))
    auto_buy_sell_info= Button(Root, image=info_icon,command=lambda : messagebox.showinfo("Auto Buy And Sell Feature Info",autobuysell_info_para))
    portfolio_btn.grid(row=4,column=1,padx=(5,0),pady=(20,0))
    auto_buy_sell_btn.grid(row=4,column=2,padx=(5,0),pady=(20,0))
    auto_buy_sell_info.grid(row=4,column=3,padx=(0,40),pady=(20,0))

    exit_btn = Button(Root,text="Exit",padx=13,pady=3,command=_Quit,font=("Arial",10,"bold"))
    exit_btn.grid(row=5,column=5,padx=(0,5),pady=(25,0))
    return

def _HowToUse():
    #How to use window
    howtouse_window= Toplevel(Root)
    #Root title,size,icon
    howtouse_window.title("How To Use | Tool")
    howtouse_window.geometry("400x300")
    howtouse_window.iconbitmap("./lib/icons/logo.ico")

    title_label = Label(howtouse_window,text="HowTouse",font=("Arial",12,"bold"),justify=CENTER)
    title_label.grid(row=1,column=1,columnspan=3,pady=10)

    

    howtouse_paragraph = Text(howtouse_window,height=10,width=43,bg="#fffeea",relief=SUNKEN)
    howtouse_paragraph.grid(row=2,column=1,columnspan=3,padx=25)
    


    donotshow_var = BooleanVar()
    donotshow_var.set(False)
    donotshow_chkbox = Checkbutton(howtouse_window,text="Do Not Show Again",variable=donotshow_var)
    donotshow_chkbox.grid(row=3,column=1,columnspan=2,pady=(20,0))

    close_btn = Button(howtouse_window,text="Close",font=("Arial",10,"bold"),command=lambda:_GeneralUpdate("HowToUse_close",donotshow_var,howtouse_window),padx=13,pady=3)
    close_btn.grid(row=3,column=3,pady=(20,0))
    return

def _TermsAndCondition():
    #Root title,size
    Root.title("Terms And Condition | Tool")
    Root.geometry("500x500")
    
    #If any delete all the previous widgets from window
    try:
        for widgets in Root.winfo_children():
            widgets.destroy()
    except:
        pass
    
    title_lb = Label(Root, text="Terms And Conditions",anchor=CENTER,font=("Arial",14,"bold"))
    title_lb.grid(row=1,column=1,columnspan=3,pady=(10,20))

    disclaimer_text = """
    This is for educational purpose only. This tool contains scraping and 
    using bots on other's site. Scraping or using bots on others side with 
    out their permission is illegal.                                
    """
    termsandcondition_text = """
    1. You must be born before June 15,1996 to use this tool.
    2. We will not be liable for any misconduct done using this tool. 
    3. Agree to the terms and condition only if you acknoledge that scraping 
       other's site without permission is illegal.
    """

    sunken_paragraph = Text(Root,relief=SUNKEN,background="#fffeea",height=20,width=55)
    sunken_paragraph.grid(row=2,column=1,columnspan=3,padx=(25,25))
    


    sunken_paragraph.tag_configure('tag-center', justify='center', font=('Arial', 12, 'bold'))
    sunken_paragraph.tag_configure('tag-left', justify='left',font=('Arial', 10))
    sunken_paragraph.tag_configure('bold')

    sunken_paragraph.insert('end', "\n"+'Disclaimer :'+"\n", 'tag-center')
    sunken_paragraph.insert('end', disclaimer_text+"\n", 'tag-left')
    sunken_paragraph.insert('end', 'Terms And Condition :'+"\n", 'tag-center')
    sunken_paragraph.insert('end', termsandcondition_text+"\n", 'tag-left')

    sunken_paragraph.config(state=DISABLED)

    check_var = BooleanVar()
    check_var.set(False)

    next_btn = Button(Root, text="Next",state=DISABLED,padx=15,pady=2,font = ("Arial",10,"bold"))
    next_btn.grid(row=3,column=3,pady=(30,0))

    agree_check_box= Checkbutton(Root, text= "Agree to terms and condition",variable=check_var,command=lambda:_GeneralUpdate("TermsAndCondition_checkbox",check_var,next_btn))
    agree_check_box.grid(row=3,column=1,columnspan=2,pady=(30,0))    

def _Main():
    
    # Setting default value false for running RunningBuy and RunningBuy

    if _Config("r","RunningBuy") != False:

        _Config("w","RunningBuy",False)
    
    if _Config("r","RunningSell") != False:

        _Config("w","RunningSell",False)

    if _Config("r","MarketOpen") != False:

        _Config("w","MarketOpen",False)

    _Config("w","MarketDataBuy",None)
    _Config("w","MarketDataSell",None)



    # Checking Chrome Driver
    threading.Thread(target=_CheckChrome).start()
    threading.Thread(target = _CreateDataBase).start()

    if _Config("r","TermsAndCondition") != True:
        #Run TermsandCondition:
        _TermsAndCondition()
        return
    if _Config("r","TermsAndCondition") == True and _Config("r","HowToUse") == False:
        #Run HowToUse
        _HomeScreen()
        _HowToUse()
        return
    _HomeScreen()

if __name__ == "__main__":
    threading.Thread(target=_RunBot).start()
    _Main()

#Root Window Loop
Root.mainloop()