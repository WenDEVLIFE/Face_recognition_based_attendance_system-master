############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
import pandas as pd
import datetime
import time
from PIL import Image, ImageTk

# Ensure working directory is the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'xxxxxxxxxxxxx@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="#121212")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='#121212',fg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="white",bg="#2D2D2D",relief='solid',font=('times', 12, ' bold '),show='*',insertbackground='white')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='#121212',fg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="white",bg="#2D2D2D",relief='solid', font=('times', 12, ' bold '),show='*',insertbackground='white')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='#121212',fg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="white",bg="#2D2D2D", relief='solid',font=('times', 12, ' bold '),show='*',insertbackground='white')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="white"  ,bg="#EF4444" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '),relief='flat')
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="white", bg="#10B981", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '),relief='flat')
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear3():
    txt3.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME', '', 'SECTION']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    section = (txt3.get())
    if ((name.isalpha()) or (' ' in name)):
        # Initialize the face detector and sample counter here
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        sampleNum = 0
        cam = cv2.VideoCapture(0)
        cam_win = tk.Toplevel(window)
        cam_win.title("Taking Images")
        cam_lbl = tk.Label(cam_win)
        cam_lbl.pack()
        
        while (True):
            if not cam_win.winfo_exists():
                break
            ret, img = cam.read()
            if not ret or img is None:
                mess._show(title='Camera Error', message='Cannot access the camera! Please ensure a webcam is connected.')
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/" + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                            
            # display the frame using Tkinter
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=img_pil)
            cam_lbl.imgtk = imgtk
            cam_lbl.configure(image=imgtk)
            cam_win.update()
            
            # break if the sample number is morethan 100
            if sampleNum > 100:
                break
        cam.release()
        if cam_win.winfo_exists():
            cam_win.destroy()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name, '', section]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
        message.configure(text='Total Registrations till now  : ' + str(serial))
        mess._show(title='Registration Successful', message='Images taken successfully for ID: ' + Id + '. Please click "Save Profile" to complete registration.')
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(len(set(ID))))
    mess._show(title='Profile Saved', message='Profile trained and saved successfully!')

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Section', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    cam_win = tk.Toplevel(window)
    cam_win.title("Taking Attendance (Close Window to Stop)")
    cam_lbl = tk.Label(cam_win)
    cam_lbl.pack()
    
    attendance = None
    while True:
        if not cam_win.winfo_exists():
            break
        ret, im = cam.read()
        if not ret or im is None:
            mess._show(title='Camera Error', message='Cannot access the camera! Please ensure a webcam is connected.')
            break
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial, 'NAME'].values[0]
                ID = df.loc[df['SERIAL NO.'] == serial, 'ID'].values[0]
                ID = str(ID)
                bb = str(aa)
                sec = df.loc[df['SERIAL NO.'] == serial, 'SECTION'].values[0]
                sec = str(sec)
                attendance = [str(ID), '', bb, '', sec, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
            
        # display the frame using Tkinter
        img_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        cam_lbl.imgtk = imgtk
        cam_lbl.configure(image=imgtk)
        cam_win.update()
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance/Attendance_" + date + ".csv")
    if attendance is not None:
        if exists:
            with open("Attendance/Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(attendance)
            csvFile1.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvFile1.close()
    with open("Attendance/Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        next(reader1, None) # Skip header row
        for lines in reader1:
            if not lines:
                continue
            iidd = str(lines[0]) + '   '
            tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]), str(lines[8])))
    csvFile1.close()
    cam.release()
    if cam_win.winfo_exists():
        cam_win.destroy()
    mess._show(title='Attendance Successful', message='Attendance has been recorded successfully!')

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

# --- Theme Colors ---
BG_COLOR = "#0b0f14"  # Darker background
FRAME_COLOR = "#111827" # Dark blue-gray for frames
TEXT_COLOR = "#FFFFFF"
ACCENT_BLUE = "#3B82F6"
ACCENT_GREEN = "#10B981"
ACCENT_RED = "#EF4444"
INPUT_BG = "#1f2937"
# --------------------

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Face Recognition Attendance System")
window.configure(background=BG_COLOR)

# Load logos
logo1 = Image.open("logo/logo1.png")
logo1 = logo1.resize((80, 80), Image.Resampling.LANCZOS)
logo1_img = ImageTk.PhotoImage(logo1)

logo2 = Image.open("logo/logo2.png")
logo2 = logo2.resize((80, 80), Image.Resampling.LANCZOS)
logo2_img = ImageTk.PhotoImage(logo2)

# Header Section
header_frame = tk.Frame(window, bg=BG_COLOR)
header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.12)

logo1_lbl = tk.Label(header_frame, image=logo1_img, bg=BG_COLOR)
logo1_lbl.place(x=50, y=5)

title_lbl = tk.Label(header_frame, text="Pamantasan ng Lungsod ng Muntinlupa", fg=TEXT_COLOR, bg=BG_COLOR, font=('times', 32, 'bold'))
title_lbl.place(relx=0.5, rely=0.5, anchor='center')

logo2_lbl = tk.Label(header_frame, image=logo2_img, bg=BG_COLOR)
logo2_lbl.place(relx=1.0, x=-130, y=5)

# Date and Time Display
date_time_frame = tk.Frame(window, bg=BG_COLOR)
date_time_frame.place(relx=0, rely=0.12, relwidth=1, relheight=0.05)

date_time_str = day + "-" + mont[month] + "-" + year + "  |  "
date_lbl = tk.Label(date_time_frame, text=date_time_str, fg=ACCENT_BLUE, bg=BG_COLOR, font=('times', 22, 'bold'))
date_lbl.pack(side='left', expand=True, padx=(200, 0))

clock = tk.Label(date_time_frame, fg=ACCENT_BLUE, bg=BG_COLOR, font=('times', 22, 'bold'))
clock.pack(side='left')
tick()

frame1 = tk.Frame(window, bg=FRAME_COLOR, bd=2, relief='ridge')
frame1.place(relx=0.02, rely=0.20, relwidth=0.47, relheight=0.78)

frame2 = tk.Frame(window, bg=FRAME_COLOR, bd=2, relief='ridge')
frame2.place(relx=0.51, rely=0.20, relwidth=0.47, relheight=0.78)

head2 = tk.Label(frame2, text="For New Registrations", fg=TEXT_COLOR, bg=ACCENT_BLUE, font=('times', 17, 'bold'))
head2.place(relx=0, rely=0, relwidth=1)

head1 = tk.Label(frame1, text="For Already Registered", fg=TEXT_COLOR, bg=ACCENT_BLUE, font=('times', 17, 'bold'))
head1.place(relx=0, rely=0, relwidth=1)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg=TEXT_COLOR  ,bg=FRAME_COLOR ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=30)

txt = tk.Entry(frame2,width=32 ,fg=TEXT_COLOR,bg=INPUT_BG,font=('times', 15, ' bold '), insertbackground=TEXT_COLOR)
txt.place(x=30, y=60)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg=TEXT_COLOR  ,bg=FRAME_COLOR ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=100)

txt2 = tk.Entry(frame2,width=32 ,fg=TEXT_COLOR,bg=INPUT_BG,font=('times', 15, ' bold ') , insertbackground=TEXT_COLOR )
txt2.place(x=30, y=130)

lbl3_sec = tk.Label(frame2, text="Enter Section",width=20  ,fg=TEXT_COLOR  ,bg=FRAME_COLOR ,font=('times', 17, ' bold '))
lbl3_sec.place(x=80, y=170)

txt3 = tk.Entry(frame2,width=32 ,fg=TEXT_COLOR,bg=INPUT_BG,font=('times', 15, ' bold ') , insertbackground=TEXT_COLOR )
txt3.place(x=30, y=200)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg=FRAME_COLOR ,fg=TEXT_COLOR  ,width=39 ,height=1, activebackground = FRAME_COLOR ,font=('times', 15, ' bold '))
message1.place(x=7, y=250)

message = tk.Label(frame2, text="" ,bg=FRAME_COLOR ,fg=TEXT_COLOR  ,width=39,height=1, activebackground = FRAME_COLOR ,font=('times', 16, ' bold '))
message.place(relx=0.5, y=530, anchor='center')

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg=TEXT_COLOR  ,bg=FRAME_COLOR  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(relx=0.5, y=115, anchor='center')

res=0
exists = os.path.isfile("StudentDetails/StudentDetails.csv")
if exists:
    with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background=INPUT_BG,
                foreground=TEXT_COLOR,
                rowheight=25,
                fieldbackground=INPUT_BG,
                bordercolor=BG_COLOR,
                borderwidth=0)
style.map('Treeview', background=[('selected', ACCENT_BLUE)])
style.configure("Treeview.Heading",
                background=BG_COLOR,
                foreground=TEXT_COLOR,
                relief="flat",
                font=('times', 12, 'bold'))
style.map("Treeview.Heading",
          background=[('active', FRAME_COLOR)])

tv= ttk.Treeview(frame1,height =13,columns = ('name','section','date','time'))
tv.column('#0',width=60)
tv.column('name',width=110)
tv.column('section',width=90)
tv.column('date',width=110)
tv.column('time',width=110)
tv.grid(row=2,column=0,padx=(20,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('section',text ='SECTION')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg=TEXT_COLOR  ,bg=ACCENT_RED  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '), relief="flat")
clearButton.place(x=335, y=58)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg=TEXT_COLOR  ,bg=ACCENT_RED  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '), relief="flat")
clearButton2.place(x=335, y=128)
clearButton3 = tk.Button(frame2, text="Clear", command=clear3  ,fg=TEXT_COLOR  ,bg=ACCENT_RED  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '), relief="flat")
clearButton3.place(x=335, y=198)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg=TEXT_COLOR  ,bg=ACCENT_BLUE  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), relief="flat")
takeImg.place(relx=0.5, y=300, anchor='center')
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg=TEXT_COLOR  ,bg=ACCENT_GREEN  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), relief="flat")
trainImg.place(relx=0.5, y=380, anchor='center')
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg=TEXT_COLOR  ,bg=ACCENT_BLUE  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), relief="flat")
trackImg.place(relx=0.5, y=50, anchor='center')
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg=TEXT_COLOR  ,bg=ACCENT_RED  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), relief="flat")
quitWindow.place(relx=0.5, y=530, anchor='center')

##################### END ######################################

def show_login_window():
    window.withdraw() # hide main window
    
    login_win = tk.Toplevel(window)
    login_win.geometry("400x260")
    login_win.resizable(False, False)
    login_win.title("Admin Login")
    login_win.configure(background=BG_COLOR)
    
    def on_closing():
        window.destroy()
        
    login_win.protocol("WM_DELETE_WINDOW", on_closing)
    
    lbl_title = tk.Label(login_win, text="System Login", bg=BG_COLOR, fg=TEXT_COLOR, font=('times', 18, 'bold'))
    lbl_title.pack(pady=15)
    
    frame_inputs = tk.Frame(login_win, bg=BG_COLOR)
    frame_inputs.pack(pady=5)
    
    lbl_user = tk.Label(frame_inputs, text="Username:", bg=BG_COLOR, fg=TEXT_COLOR, font=('times', 12, 'bold'))
    lbl_user.grid(row=0, column=0, padx=10, pady=5, sticky='e')
    
    ent_user = tk.Entry(frame_inputs, width=20, bg=INPUT_BG, fg=TEXT_COLOR, font=('times', 12, 'bold'), insertbackground=TEXT_COLOR)
    ent_user.insert(0, "admin")
    ent_user.grid(row=0, column=1, padx=10, pady=5)
    
    lbl_pass = tk.Label(frame_inputs, text="Password:", bg=BG_COLOR, fg=TEXT_COLOR, font=('times', 12, 'bold'))
    lbl_pass.grid(row=1, column=0, padx=10, pady=5, sticky='e')
    
    ent_pass = tk.Entry(frame_inputs, width=20, bg=INPUT_BG, fg=TEXT_COLOR, font=('times', 12, 'bold'), show='*', insertbackground=TEXT_COLOR)
    ent_pass.grid(row=1, column=1, padx=10, pady=5)
    
    def validate_login():
        user = ent_user.get()
        pwd = ent_pass.get()
        
        saved_pwd = "admin"
        if os.path.isfile("TrainingImageLabel/psd.txt"):
            with open("TrainingImageLabel/psd.txt", "r") as tf:
                saved_pwd = tf.read().strip()
                
        if user == "admin" and pwd == saved_pwd:
            login_win.destroy()
            window.deiconify() # Show main window
        else:
            mess._show(title='Login Failed', message='Incorrect Username or Password!')
            
    btn_login = tk.Button(login_win, text="Login", command=validate_login, fg=TEXT_COLOR, bg=ACCENT_BLUE, width=15, font=('times', 12, 'bold'), relief='flat')
    btn_login.pack(pady=15)

show_login_window()

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
