#Imports
from ctypes import alignment
import json
from msilib.schema import CheckBox, ComboBox, Font
from re import search
# GUI
from tkinter import *
from tkinter import font, messagebox,ttk
# GUI Icon
from PIL import Image,ImageTk

#Load Config file
with open ("./data/config.json","r") as read_config:
    Config=json.load(read_config)

stock_list = ["(RLFL) Reliance Finance Ltd.","(NIFRA) Nepal Infrastructure Bank Limited","(NABIL) Nabil Bank Limited" ]

#Root Window
Root = Tk()
Root.iconbitmap("./lib/icons/logo.ico")

#Fonts
font_btn = ("Arial",10)
font_lb = ("Arial",10)

#Icon
setting_icon_temp = Image.open("./lib/icons/settings.png")
setting_icon_temp=setting_icon_temp.resize((28,28),Image.ANTIALIAS)
home_icon_temp = Image.open("./lib/icons/home.png")
info_icon_temp=home_icon_temp.resize((20,20),Image.ANTIALIAS)
info_icon_temp = Image.open("./lib/icons/info.png")
info_icon_temp=info_icon_temp.resize((20,20),Image.ANTIALIAS)
setting_icon = ImageTk.PhotoImage(setting_icon_temp)         
home_icon = ImageTk.PhotoImage(home_icon_temp)         
info_icon = ImageTk.PhotoImage(info_icon_temp)         

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
    


    calculator_btn = Button(Root,text="Calculator",font=font_btn,padx=13,pady=3)
    setting_btn = Button(Root,image=setting_icon)
    calculator_btn.grid(row=1,column=1,padx=(15,0),pady=(25,0))
    setting_btn.grid(row=1,column=5,pady=(25,0),padx=(0,15))

    search_script_info_para="""
Use this feature to search any stock listed on NEPSE.
This shows basic information about the stock.
    """
    search_script_var = StringVar()
    search_script_lb = Label(Root,text="Search Stock : ",font=font_lb)
    search_script_ety = ttk.Combobox(Root,value=stock_list)
    search_script_ety.config(width=30,height=3,textvariable=search_script_var)
    search_script_ety.bind("<KeyRelease>",lambda e: _Update("HomeScreen_stocksearch",search_script_var,search_script_ety))
    #search_script_ety.bind("<Return>",lambda e: SEARCH))
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
    auto_buy_sell_btn = Button(Root,text="Auto Buy & Sell",padx=13,pady=3,font=font_btn)
    auto_buy_sell_info= Button(Root, image=info_icon,command=lambda : messagebox.showinfo("Auto Buy And Sell Feature Info",autobuysell_info_para))
    portfolio_btn.grid(row=4,column=1,padx=(5,0),pady=(20,0))
    auto_buy_sell_btn.grid(row=4,column=2,padx=(5,0),pady=(20,0))
    auto_buy_sell_info.grid(row=4,column=3,padx=(0,40),pady=(20,0))

    exit_btn = Button(Root,text="Exit",padx=13,pady=3,command=quit,font=("Arial",10,"bold"))
    exit_btn.grid(row=5,column=5,padx=(0,5),pady=(25,0))
    return

def _Update(_todo,_a=None,_b=None):
    
    if _todo == "TermsAndCondition_checkbox":
        #Update next button

        check = _a.get()
        if check != True:
            _b.destroy() #destroy next btn
            next_btn = Button(Root, text="Next",state=DISABLED,padx=15,pady=2)
            next_btn.grid(row=3,column=3,pady=(30,0))
            return
        _b.destroy() #destroy next btn
        next_btn = Button(Root, text="Next",command=lambda:_Update("TermsAndCondition_btn"),padx=15,pady=2)
        next_btn.grid(row=3,column=3,pady=(30,0))
        return
    if _todo == "TermsAndCondition_btn":

        # Update config 
        Config['TermsAndCondition'] = True
        with open ("./data/config.json","w") as write:
            json.dump(Config,write)
        write.close()
        if Config["HowToUse"] == False:
            _HomeScreen()
            _HowToUse()
            return
        _HomeScreen()
        return

    if _todo == "HowToUse_close" :
        check_donotshow = _a.get()
        #_b = howtouse_window

        if check_donotshow == True:
            Config["HowToUse"] = True
            with open("./data/config.json","w") as write_config:
                json.dump(Config,write_config)
            write_config.close()
            _b.destroy()
            _HomeScreen()
            return
        _b.destroy()
        _HomeScreen()

    if _todo=="HomeScreen_stocksearch":
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

    close_btn = Button(howtouse_window,text="Close",font=("Arial",10,"bold"),command=lambda:_Update("HowToUse_close",donotshow_var,howtouse_window),padx=13,pady=3)
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

    next_btn = Button(Root, text="Next",state=DISABLED,padx=15,pady=2)
    next_btn.grid(row=3,column=3,pady=(30,0))

    agree_check_box= Checkbutton(Root, text= "Agree to terms and condition",variable=check_var,command=lambda:_Update("TermsAndCondition_checkbox",check_var,next_btn))
    agree_check_box.grid(row=3,column=1,columnspan=2,pady=(30,0))    

def _Main():
    
    if Config["TermsAndCondition"] != True:
        #Run TermsandCondition:
        _TermsAndCondition()
    
    if Config["TermsAndCondition"] == True and Config["HowToUse"] == False:
        #Run HowToUse
        _HomeScreen()
        _HowToUse()
        return
    _HomeScreen()


_Main()
#Root Window Loop
Root.mainloop()