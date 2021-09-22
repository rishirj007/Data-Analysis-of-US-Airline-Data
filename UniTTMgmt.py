import re
import tkinter
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
#KindlyFocusHere


#giving username="123alpha456" and password="monibuvyze" opens register window


#database connectivity logic starts
convar=mysql.connector.connect(host='localhost',user='root',passwd='',database='UTTMS')
mycur=convar.cursor()
#database connectivity logic ends


#window containers space starts
loginwindow=None
homewindow=None
editcourseswindow=None
editsubjectswindow=None
editteacherswindow=None
assignteacherswindow=None

createtablewindow=None

loginwindowframe=None
topframe=None
mainframe=None
recentframe=None
clashframe=None
#window containers space ends


#window variable space starts
currentdept=None
loginusername_txt=None
loginpassword_txt=None
insname='Sri Guru Granth Sahib World Univesity'
course=None
substream=None
batch=None
sem=None
sflag=False
rnotxt=None
count=0

mondayvar=[]
tuesdayvar=[]
wednesdayvar=[]
thursdayvar=[]
fridayvar=[]


#window variable space ends

#loginwindow method space starts
def loginfun():
    global loginusername_txt
    global loginpassword_txt
    global currentdept
    global mycur
    global convar
    
    if(len(loginusername_txt.get())==0 or len(loginpassword_txt.get())==0):
        messagebox.showinfo('Error','Kindly fill all the Fields')
    else:
        mycur.execute("select * from deptinfo where Username='"+loginusername_txt.get()+"'")
        currentdept=mycur.fetchall()
        if(len(currentdept)>0):
            if(currentdept[0][3]==loginpassword_txt.get()):
                mycur.execute("show tables like'"+currentdept[0][1]+"'")
                dflag=mycur.fetchall()
                if(len(dflag)==0):
                    mycur.execute("create table "+currentdept[0][1]+" (cname varchar(255),ccode varchar(255) unique,msem int)")
                    convar.commit()
                homewindowopener()
            else:
                messagebox.showinfo('Error','Incorrect Password')
        else:
            if(loginusername_txt.get()=="123alpha456" and loginpassword_txt.get()=="monibuvyze"):
                regerer()
            else:
                messagebox.showinfo('Error','Account does not exist')
        
#loginwindow method space ends
def regerer():
    def register():
        global mycur
        global convar
        Dacronym=''.join(w[0] for w in deptn.get().lower().split())
        rows=finder()
        flag=False
        if Dacronym in rows:
            for i in range(1,5):
                temp=Dacronym+str(i)
                if temp in rows:
                    pass
                else:
                    Dacronym=temp
                    flag=True
                    break
        else:
            try:
                mycur.execute("insert into deptinfo values('"+deptn.get()+"','"+Dacronym+"','"+usern.get()+"','"+passw.get()+"')")
                convar.commit()
                messagebox.showinfo('Success','Added')
                regwin.destroy()
            except mysql.connector.Error as err:
                messagebox.showinfo('Database Error',err.msg)
        if(flag==True):
            try:
                mycur.execute("insert into deptinfo values('"+deptn.get()+"','"+Dacronym+"','"+usern.get()+"','"+passw.get()+"')")
                convar.commit()
                messagebox.showinfo('Success','Added')
                regwin.destroy()
            except mysql.connector.Error as err:
                messagebox.showinfo('Database Error',err.msg)
            
    def finder():
        global mycur
        mycur.execute("select Abbreviation from deptinfo")
        temp=mycur.fetchall()
        temp2=[]
        for i in range(0,len(temp)):
            temp2.append(temp[i][0])
        return temp2
    
    global loginwindow
    loginwindow.destroy()
    regwin=tkinter.Tk()

    deptn=tkinter.StringVar(regwin)
    usern=tkinter.StringVar(regwin)
    passw=tkinter.StringVar(regwin)
    
    lblname=tkinter.Label(regwin,text="Dept Name")
    lblname.pack()
    dptname=tkinter.Entry(regwin,textvariable=deptn)
    dptname.pack(padx=20,ipadx=50)
    lblname=tkinter.Label(regwin,text="Username")
    lblname.pack()
    dptadmin=tkinter.Entry(regwin,textvariable=usern)
    dptadmin.pack(padx=20,ipadx=50)
    lblname=tkinter.Label(regwin,text="Password")
    lblname.pack()
    dptpass=tkinter.Entry(regwin,textvariable=passw)
    dptpass.pack(padx=20,ipadx=50)
    regbtn=tkinter.Button(regwin,text="Register",command=register)
    regbtn.pack()
#homewindow method space starts

def editCoursesWindowOpener():
    global editcourseswindow
    if(editcourseswindow!=None):
        editcourseswindow.destroy()
        editcourseswindowcreator()
    else:
        editcourseswindowcreator()
    
def editSubjectsWindowOpener():
    global course
    global mycur
    global convar
    global currentdept
    if(course.get()=="--select--"):
        messagebox.showinfo("Error","Kindly select a course ")
    else:
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()

        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"

        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            editsubjectswindowcreator()
        else:
            mycur.execute("create table "+temp+" (sname varchar(255),scode varchar(255) unique,slab boolean,teacher varchar(255))")
            convar.commit()
            editsubjectswindowcreator()
def editTeachersWindowOpener():
    editteacherswindowcreator()
    
def assignTeachersWindowOpener():
    global course
    if(course.get()=="--select--"):
        messagebox.showinfo("Error","Kindly select a course ")
    else:
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()

        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"

        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        dat=[]
        if(len(dflag)==1):
            mycur.execute("select * from "+temp)
            dat=mycur.fetchall()
        if(len(dat)!=0):
            tbl=currentdept[0][1]+"teachers"
            mycur.execute("show tables like '"+tbl+"'")
            flag=mycur.fetchall()
            if(len(flag)==1):
                assignteacherswindowcreator()
            else:
                messagebox.showinfo('Error','Teacher data not found.\nKindly upload Teacher data via Edit menu')
        else:
            messagebox.showinfo('Error','Subjects not found.\nKindly add subjects via Edit menu')
        
    
def searchtable():
    global course
    global batch
    global sem
    global currentdept
    global sflag
    if(course.get()=="--select--"):
        messagebox.showinfo("Error","Kindly select a course ")
    else:
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()

        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()

        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            sflag=True
            createtablewindowopener()
        else:
            messagebox.showinfo('Search Result','TimeTable for '+course.get()+' Batch '+batch.get()+' Sem '+sem.get()+' does not exist')
def createtable():
    global course
    global batch
    global sem
    global currentdept
    global sflag
    if(course.get()=="--select--"):
        messagebox.showinfo("Error","Kindly select a course ")
    else:
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()

        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()

        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            messagebox.showinfo('Error','Timetable already exists')
        else:
            sflag=False
            tsub=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
            mycur.execute("show tables like '"+tsub+"'")
            sub=mycur.fetchall()
            if(len(sub)==1):
                mycur.execute("select teacher from "+sub[0][0])
                teachers=mycur.fetchall()
                if(len(teachers)>0):
                    clear=True
                    for one in teachers:
                        if(one[0]=="notAssigned"):
                            messagebox.showinfo('Error','All subjects must have a teacher assigned.\nKindly Edit and Assign teachers via Edit menu')
                            clear=False
                            break
                    if(clear==True):
                        tvarclear()
                else:
                    messagebox.showinfo("Error","Subjects not found.\nKindly add subjects via Edit menu")
            else:
                messagebox.showinfo('Error','Subjects not found.\nKindly add subjects via Edit menu')
                

def tvarclear():
    global mondayvar
    global tuesdayvar
    global wednesdayvar
    global thursdayvar
    global fridayvar
    mondayvar=[]
    tuesdayvar=[]
    wednesdayvar=[]
    thursdayvar=[]
    fridayvar=[]
    createtablewindowopener()
def deletetable():
    global course
    global batch
    global sem
    global currentdept
    global mycur
    global convar
    if(course.get()=="--select--"):
        messagebox.showinfo("Error","Kindly select a course ")
    else:
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()

        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()

        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            messagebox.showinfo('Database','Timetable deleted')
            mycur.execute("drop table "+temp)
            convar.commit()
        else:
            messagebox.showinfo('Database','TimeTable for '+course.get()+' Batch '+batch.get()+' Sem '+sem.get()+' does not exist')
def updatetable():
    global sflag
    global convar
    global mycur
    global currentdept
    
    if(course.get()=="--select--"):
        messagebox.showinfo("Error","Kindly select a course ")
    else:
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()

        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()

        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            sflag=False
            createtablewindowopener()
        else:
            messagebox.showinfo('Error','Timetable for '+course.get()+' Batch '+batch.get()+' Sem '+sem.get()+' does not exist')
def tvarfill(name):
    print(name)
    global currentdept
    global mondayvar
    global tuesdayvar
    global wednesdayvar
    global thursdayvar
    global fridayvar
    global rnotxt

    global mycur
    
    mycur.execute("show tables like '"+name+"'")
    dflag=mycur.fetchall()
    table=currentdept[0][1]+"rnotable"
    if(len(dflag)==1):
        mycur.execute("select room from "+table+" where class='"+name+"'")
        data=mycur.fetchall()
        rnotxt.set(data[0][0])
        mycur.execute("select * from "+name)
        table=mycur.fetchall()
        i=0
        for cell in table[0]:
            mondayvar[i].set(cell)
            i+=1
        i=0
        for cell in table[1]:
            tuesdayvar[i].set(cell)
            i+=1
        i=0
        for cell in table[2]:
            wednesdayvar[i].set(cell)
            i+=1
        i=0
        for cell in table[3]:
            thursdayvar[i].set(cell)
            i+=1
        i=0
        for cell in table[4]:
            fridayvar[i].set(cell)
            i+=1
            
#homewindow method space ends

def addcourse(cname,ccode,msem):
    global currentdept

    global mycur
    global convar
    while(True):
        mycur.execute("show tables like '"+currentdept[0][1]+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            if(len(cname)==0 or len(ccode)==0 or len(msem)==0):
                messagebox.showinfo("Database","Kindly fill all the fields")
                break
            else:
                try:
                    mycur.execute("insert into "+dflag[0][0]+ " values ('"+cname+"','"+ccode+"','"+msem+"')")
                    convar.commit()
                    messagebox.showinfo("Database","Course Addition Sucessful")
                    break
                except mysql.connector.Error as err:
                    messagebox.showinfo('Database Error',err.msg)
                    break
        else:
            mycur.execute("create table "+currentdept[0][1]+" (cname varchar(255),ccode varchar(255) unique,msem int)")
            convar.commit()
    
def addsubject(sname,scode,slab):
    global mycur
    global convar
    global course
    global batch
    global sem
    global currentdept

    while(True):
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()
        temp=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()

        if(len(dflag)==1):
            if(len(sname)==0 or len(scode)==0):
                messagebox.showinfo("Database","Kindly fill all the fields")
                break
            else:
                try:
                    mycur.execute("insert into "+dflag[0][0]+ " values ('"+sname+"','"+scode+"',%s,'notAssigned')"%(int(slab)))
                    convar.commit()
                    messagebox.showinfo("Database","subject Sucessfully Added")
                    break
                except mysql.connector.Error as err:
                    messagebox.showinfo('Database Error',err.msg)
                    break
                    
        else:
            print("in Db not found, creating")
            mycur.execute("create table "+temp+" (sname varchar(255),scode varchar(255) unique,slab boolean,teacher varchar(255))")
            convar.commit()
    
def addteacher(tid,tname,tmail):
    global mycur
    global convar
    global currentdept
    while(True):
        temp=currentdept[0][1]+"teachers"
        mycur.execute("show tables like '"+temp+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            if(len(tname)==0 or len(tmail)==0):
                messagebox.showinfo("Database","Kindly fill all the fields")
                break
            else:
                try:
                    mycur.execute("insert into "+dflag[0][0]+ " values ('"+tid+"','"+tname+"','"+tmail+"')")
                    convar.commit()
                    messagebox.showinfo("Database","Teacher Sucessfully Added")
                    break
                except mysql.connector.Error as err:
                    messagebox.showinfo('Database Error',err.msg)
                    break
        else:
            mycur.execute("create table "+currentdept[0][1]+ "teachers (tid varchar(255) unique,tname varchar(255),tmail varchar(255))")
            convar.commit()

def assignteacher(tid,scode):
    global mycur
    global convar
    global currentdept
    if(tid=="--select--" or scode=="--select--"):
        messagebox.showinfo("Error","Kindly select something in all fields")
    else:
        try:
            mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
            code=mycur.fetchall()
                
            tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"

            mycur.execute("update "+tempo+" set teacher = '"+tid+"' where scode='"+scode+"'")
            convar.commit()
            messagebox.showinfo("Success","Teacher Assigned")
        except mysql.connector.Error as err:
                    messagebox.showinfo('Database Error',err.msg)

#loginwindow space starts
def loginwindowopener():
    loginwindowcreator()
def loginwindowcreator():
    
    global loginwindow
    global loginwindowframe
    global loginusername_txt
    global loginpassword_txt

    loginwindow=tkinter.Tk()
    loginwindow.geometry('450x650+700+200')
    loginwindow.title('University TimeTable Management System')
    loginwindow.config(bg='#FFD700')
    loginwindow.resizable(width=False,height=False)

    loginwindowframe=tkinter.LabelFrame(loginwindow,width=500,padx=25,pady=25,bg='#FFFFFF')
    loginwindowframe.pack(anchor='n',fill='y',expand=True)

    loginusername_txt=tkinter.StringVar()
    loginpassword_txt=tkinter.StringVar()

    name=tkinter.Label(loginwindowframe,text="University\nTime-Table\nManagement\nSystem",relief="groove",bg="#FFD700",font=("Courier",14))
    name.pack(pady=10,fill='x')
    loginusernamelabel=tkinter.Label(loginwindowframe,anchor='w',text='Username',font=("",12),bg='#FFFFFF')
    loginusernamelabel.pack(fill='x')
    loginusername=tkinter.Entry(loginwindowframe,textvariable=loginusername_txt,font=("",14),foreground="#1167B1",relief="solid")
    loginusername.pack(pady=20,)

    loginpasswordlabel=tkinter.Label(loginwindowframe,anchor='w',text='Password',font=("",12),bg='#FFFFFF')
    loginpasswordlabel.pack(fill='x')
    loginpassword=tkinter.Entry(loginwindowframe,textvariable=loginpassword_txt,font=("",14),foreground="#1167B1",relief="solid",show='*')
    loginpassword.pack(pady=20)

    loginbutton=tkinter.Button(loginwindowframe,text='LOG IN',command=loginfun,bg='#FFFFFF',font=("",12),relief="groove",activebackground="#FFD700")
    loginbutton.pack(pady=20,fill='x')
#loginwindow space ends

#homewindow space starts
def homewindowopener():
    global loginwindow
    loginwindow.destroy()
    homewindowcreator()
    
def homewindowcreator():
    global homewindow
    global topframe
    global mainframe
    global recentframe
    global clashframe
    
    global insname
    global currentdept
    global course
    global batch
    global sem
    global substream

    global mycur
    global convar

    
    def updatecourselist():
        global currentdept
        global mycur
        mycur.execute("select cname from "+currentdept[0][1])
        temp=mycur.fetchall()
        temp2=[]
        for data in temp:
            temp2.append(data[0])
        coursedroplist["values"]=temp2

    def quitter():
        global homewindow
        homewindow.destroy()
    homewindow=tkinter.Tk()
    homewindow.config(bg='#FFFFFF')
    #homewindow.geometry('1100x720')
    homewindow.title('University TimeTable Management System')
    homewindow.resizable(height=False,width=False)

    menubar=tkinter.Menu(homewindow)
    homewindow.config(menu=menubar)

    file_menu=tkinter.Menu(menubar)
    menubar.add_cascade(label="File",menu=file_menu)
    file_menu.add_command(label="Logout",command=logout)
    file_menu.add_command(label="Exit",command=quitter)
    

    edit_menu=tkinter.Menu(menubar)
    menubar.add_cascade(label="Edit",menu=edit_menu)
    edit_menu.add_command(label="Edit Courses ",command=editCoursesWindowOpener)
    edit_menu.add_command(label="Edit Subjects for current selection",command=editSubjectsWindowOpener)
    edit_menu.add_command(label="Edit Teachers",command=editTeachersWindowOpener)
    edit_menu.add_command(label="Assign Teachers for current selection",command=assignTeachersWindowOpener)
    
    topframe=tkinter.LabelFrame(homewindow,padx=25,pady=25,bg='#1167B1')
    topframe.pack(anchor='n',fill='x')
    mainframe=tkinter.LabelFrame(homewindow,text='Operations',padx=50,pady=25,bg='#FFD700')
    mainframe.pack(anchor='n',fill='x')
    
    clashframe=tkinter.LabelFrame(homewindow,text='Clashing',padx=25,pady=25,bg='#FFD700')
    clashframe.pack(anchor='n',fill='x')
    
    mainlabel=tkinter.Label(topframe,text=insname,anchor='w',bg='#1167B1',foreground="#FFD700")#here
    mainlabel.pack()
    mainlabel.config(font=("Courier",20,"bold"))

    deptlabel=tkinter.Label(topframe,text=currentdept[0][0],bg='#1167B1',foreground="#FFFFFF")
    deptlabel.pack()
    deptlabel.config(font=("",14))
    
    homeusertxt='Logged in as - '+currentdept[0][2]
    homeuserlabel=tkinter.Label(topframe,text=homeusertxt,bg='#1167B1',foreground="#FFFFFF")
    homeuserlabel.pack()
    homeuserlabel.config(font=("",12))

    lblcourse=tkinter.Label(mainframe,text="Course",font=("",12),padx=40,bg='#FFD700')
    lblcourse.grid(row=0,column=0,sticky='w')
    lblbatch=tkinter.Label(mainframe,text="Batch",font=("",12),padx=40,bg='#FFD700')
    lblbatch.grid(row=0,column=2,sticky='w')
    lblsem=tkinter.Label(mainframe,text="Semester",font=("",12),padx=40,bg='#FFD700')
    lblsem.grid(row=0,column=3,sticky='w')
    
    course=tkinter.StringVar(homewindow)
    courseoptions=["--select--"]
    coursedroplist=ttk.Combobox(mainframe,textvariable=course,values=courseoptions,state="readonly",width=70,postcommand=updatecourselist)
    coursedroplist.current(0)
    coursedroplist.grid(row=1,column=0,padx=35,pady=5,columnspan=2,sticky='w')#.place(relx=0.2,y=160)

    batch=tkinter.StringVar(homewindow)
    batchoptions=("2015","2016","2017","2018","2019","2020")
    batchdroplist=ttk.Combobox(mainframe,textvariable=batch,values=batchoptions,state="readonly",width=20)
    batchdroplist.grid(row=1,column=2,padx=35,pady=5)#.place(relx=0.2,y=200)
    batchdroplist.current(0)

    sem=tkinter.StringVar(homewindow)
    semoptions=("1","2","3","4","5","6","7","8","9","10")
    semdroplist=ttk.Combobox(mainframe,textvariable=sem,values=semoptions,state="readonly",width=20)
    semdroplist.grid(row=1,column=3,padx=35,pady=5)#.place(relx=0.2,y=240)
    semdroplist.current(0)

    searchbtn_home=tkinter.Button(mainframe,text="SEARCH & OPEN",width=20,font=("",10,'bold'),relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",command=searchtable)
    searchbtn_home.grid(row=2,column=0,padx=20,pady=20,sticky='n')

    newtablebtn_home=tkinter.Button(mainframe,text="CREATE TIMETABLE",width=20,font=("",10,'bold'),relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",command=createtable)
    newtablebtn_home.grid(row=2,column=1,padx=20,pady=20,sticky='n')

    deltablebtn_home=tkinter.Button(mainframe,text="DELETE TIMETABLE",width=20,font=("",10,'bold'),relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",command=deletetable)
    deltablebtn_home.grid(row=2,column=2,padx=20,pady=20,sticky='n')

    updatetablebtn_home=tkinter.Button(mainframe,text="UPDATE TIMETABLE",font=("",10,'bold'),relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",width=20,command=updatetable)
    updatetablebtn_home.grid(row=2,column=3,padx=20,pady=20,sticky='n')

    logout_home=tkinter.Button(homewindow,text="LOG OUT",relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFD700",activeforeground="#FFFFFF",command=logout)
    logout_home.place(relx=0.9,y=100,height=30,width=80,anchor='ne')


def logout():
    homewindow.destroy()
    loginwindowopener()
    
#homewindow space ends

#editcourseswindow space starts
def editcourseswindowcreator():
    global editcourseswindow
    global course
    global substream
    global batch
    global sem
    global currentdept
    global mycur
    global convar
    
    def updatelist():
        if(len(existinglist.size())!=0):
            for i in existinglist.get_children():
                existinglist.delete(i)
        mycur.execute("select * from "+currentdept[0][1])
        dtable=mycur.fetchall()
        for i in range(0,len(dtable)):
            existinglist.insert("",i+1,text=i+1,values=dtable[i])
    def delentry():
        if(len(existinglist.focus())==0):
            pass
        else:
            ctbd=existinglist.item(existinglist.focus())['values'][1]
            cctbd=existinglist.item(existinglist.focus())['values'][0]
            mycur.execute("select ccode from "+currentdept[0][1])
            bar=mycur.fetchall()
            if ctbd in bar:
                mycur.execute("delete from "+currentdept[0][1]+" where ccode='"+str(ctbd)+"'")
                convar.commit()
                existinglist.delete(existinglist.focus())
                messagebox.showinfo('Database','Course data Deleted')
            else:
                mycur.execute("delete from "+currentdept[0][1]+" where cname='"+str(cctbd)+"'")
                convar.commit()
                existinglist.delete(existinglist.focus())
                messagebox.showinfo('Database','Course data Deleted')
    editcourseswindow=tkinter.Toplevel(homewindow)#here------------------------------------
    editcourseswindow.transient(homewindow)
    editcourseswindow.grab_set()
    editcourseswindow.title('Edit Courses')
    editcourseswindow.resizable(height=False,width=False)
    top=tkinter.LabelFrame(editcourseswindow,padx=20,pady=10,bg='#1167B1')
    top.pack(fill='x',expand=True)
    headingtxt=currentdept[0][0]
    heading=tkinter.Label(top,text=headingtxt,font=("Courier",14,"bold"),bg='#1167B1',fg="#FFFFFF")
    heading.pack()

    bottom=tkinter.LabelFrame(editcourseswindow,padx=20,pady=20,bg='#FFD700')
    bottom.pack(fill='x',expand=True)

    lblcname=tkinter.Label(bottom,text="Course",anchor='w',width=20,bg='#FFD700',font=("",11))
    lblcname.grid(row=0,column=0,ipadx=70,padx=10)
    
    lblccode=tkinter.Label(bottom,text="Course Code",anchor='w',width=15,bg='#FFD700',font=("",11))
    lblccode.grid(row=0,column=1)
    
    lblcmsem=tkinter.Label(bottom,text="Max. Semesters",anchor='w',width=15,bg='#FFD700',font=("",11))
    lblcmsem.grid(row=0,column=2)

    
    cnametxt=tkinter.StringVar(editcourseswindow)
    cname=tkinter.Entry(bottom,textvariable=cnametxt)
    cname.grid(row=1,column=0,ipadx=100)
    
    ccodetxt=tkinter.StringVar(editcourseswindow)
    ccode=tkinter.Entry(bottom,textvariable=ccodetxt)
    ccode.grid(row=1,column=1,padx=2,ipadx=5)
    
    cmsemtxt=tkinter.StringVar(editcourseswindow)
    cmsem=tkinter.Entry(bottom,textvariable=cmsemtxt)
    cmsem.grid(row=1,column=2,padx=10,ipadx=5)

    addbtn=tkinter.Button(bottom,text="ADD",command=lambda: [addcourse(cnametxt.get(),ccodetxt.get(),cmsem.get()),
                                                             cname.delete(0,'end'),ccode.delete(0,'end'),cmsem.delete(0,'end'),
                                                             updatelist()],
                          relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1")
    addbtn.grid(row=2,column=2,pady=5,ipadx=17)
    
    bottommost=tkinter.LabelFrame(editcourseswindow,padx=20,pady=20,bg='#FFD700')
    bottommost.pack(fill='x',expand=True)
    
    existinglist=ttk.Treeview(bottommost)
    existinglist["columns"]=("Column 2","Column 3","Column 4")
    existinglist.column("#0",width=50,minwidth=50)
    existinglist.column("Column 2",width=150,minwidth=150)
    existinglist.column("Column 3",width=100,minwidth=100)
    existinglist.column("Column 4",width=100,minwidth=100)

    existinglist.heading("#0",text="S. no.",anchor='w')
    existinglist.heading("Column 2",text="Course",anchor='w')
    existinglist.heading("Column 3",text="Course Code",anchor='w')
    existinglist.heading("Column 4",text="Max. Semesters",anchor='w')

    
    mycur.execute("select * from "+currentdept[0][1])
    dtable=mycur.fetchall()
    
    for i in range(0,len(dtable)):
        te=""+dtable[i][1]
        dtable1=(dtable[i][0],te,dtable[i][2])
        existinglist.insert("",i,i,text=i+1,values=[dtable1[0],""+dtable1[1]+"",dtable1[2]])

    
    existinglist.pack(fill='x')
    delbtn=tkinter.Button(bottommost,text="Delete",relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",command=delentry)
    delbtn.pack(side='right',ipadx=20,padx=20,pady=20)

    info=tkinter.Label(bottommost,text="Select entry from list to Delete",anchor='e',bg='#FFD700')
    info.pack(side='right')

    
    
#editcourseswindow space ends
    
#editsubjectswindow space starts
def editsubjectswindowcreator():
    global editsubjectswindow
    global course
    global batch
    global sem
    
    def updatelist():
        if(len(existinglist.size())!=0):
            for i in existinglist.get_children():
                existinglist.delete(i)
        mycur.execute("select * from "+tempo)
        dtable=mycur.fetchall()
        for i in range(0,len(dtable)):
            if(dtable[i][2]==0):
                boo=False
            else:
                boo=True
            dtable1=[dtable[i][0],dtable[i][1],boo]
            existinglist.insert("",i+1,text=i+1,values=dtable1)

    def delentry():
        if(len(existinglist.focus())==0):
            pass
        else:
            ctbd=existinglist.item(existinglist.focus())['values'][1]
            mycur.execute("delete from "+tempo+" where scode='"+str(ctbd)+"'")
            convar.commit()
            existinglist.delete(existinglist.focus())
            messagebox.showinfo('Database','Subject data Deleted')
            
    editsubjectswindow=tkinter.Toplevel(homewindow)
    editsubjectswindow.title('Edit Subjects')
    editsubjectswindow.resizable(height=False,width=False)
    editsubjectswindow.transient(homewindow)
    editsubjectswindow.grab_set()
    top=tkinter.LabelFrame(editsubjectswindow,padx=20,pady=20,bg="#1167B1")
    top.pack(fill='x',expand=True)
    
    headingtxt=course.get()+' Batch '+batch.get()+' Sem '+sem.get()
    print(headingtxt)
    heading=tkinter.Label(top,text=headingtxt,font=("Courier",14),bg="#1167B1",fg="#FFFFFF")
    heading.pack()

    bottom=tkinter.LabelFrame(editsubjectswindow,padx=20,pady=20,bg="#FFD700")
    bottom.pack(fill='x',expand=True)

    lblsname=tkinter.Label(bottom,text="Subject Name",anchor='w',width=20,bg="#FFD700")
    lblsname.grid(row=0,column=0)
    
    lblscode=tkinter.Label(bottom,text="Subject Code",anchor='w',width=20,bg="#FFD700")
    lblscode.grid(row=0,column=1)

    snametxt=tkinter.StringVar(editsubjectswindow)
    sname=tkinter.Entry(bottom,textvariable=snametxt)
    sname.grid(row=1,column=0,padx=2,ipadx=17)
    
    scodetxt=tkinter.StringVar(editsubjectswindow)
    scode=tkinter.Entry(bottom,textvariable=scodetxt)
    scode.grid(row=1,column=1,padx=2,ipadx=17)
    
    slab=tkinter.IntVar(editsubjectswindow)
    slabcb=tkinter.Checkbutton(bottom,text="Is this a Lab subject?",bg="#FFD700",variable=slab,onvalue=1,offvalue=0)
    slabcb.grid(row=2,column=0)
    
    addbtn=tkinter.Button(bottom,text="ADD",command=lambda: [addsubject(snametxt.get(),scodetxt.get(),slab.get()),
                                                             sname.delete(0,'end'),scode.delete(0,'end'),slab.set(0),
                                                             updatelist()],
                          relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1")
    addbtn.grid(row=1,column=2,padx=50,pady=5,ipadx=17)

    bottommost=tkinter.LabelFrame(editsubjectswindow,padx=20,pady=20,bg="#FFD700")
    bottommost.pack(fill='x',expand=True)

    existinglist=ttk.Treeview(bottommost)
    existinglist["columns"]=("Column 2","Column 3","Column 4")
    existinglist.column("#0",width=50,minwidth=50)
    existinglist.column("Column 2",width=150,minwidth=150)
    existinglist.column("Column 3",width=100,minwidth=100)
    existinglist.column("Column 4",width=100,minwidth=100)

    existinglist.heading("#0",text="S. no.",anchor='w')
    existinglist.heading("Column 2",text="Subject Name",anchor='w')
    existinglist.heading("Column 3",text="Subject Code",anchor='w')
    existinglist.heading("Column 4",text="Lab Subject",anchor='w')

    mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
    code=mycur.fetchall()
            
    tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
    mycur.execute("show tables like '"+tempo+"'")
    dflag=mycur.fetchall()
    if(len(dflag)==1):
        mycur.execute("select * from "+tempo)
        dtable=mycur.fetchall()
    
        for i in range(0,len(dtable)):
            if(dtable[i][2]==0):
                boo=False
            else:
                boo=True
            dtable1=[dtable[i][0],dtable[i][1],boo]
            existinglist.insert("",i+1,text=i+1,values=dtable1)

    existinglist.pack(fill='x')

    delbtn=tkinter.Button(bottommost,text="Delete",relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",command=delentry)
    delbtn.pack(side='right',padx=20,pady=20)

#editteacherswindow space ends

def editteacherswindowcreator():
    global editteacherswindow
    global currentdept

    def updatelist():
        if(len(existinglist.size())!=0):
            for i in existinglist.get_children():
                existinglist.delete(i)
        mycur.execute("select * from "+tbl)
        dtable=mycur.fetchall()
        for i in range(0,len(dtable)):
            existinglist.insert("",i+1,text=i+1,values=dtable[i])

    def delentry():
        if(len(existinglist.focus())==0):
            print('nothing')
        else:
            ctbd=existinglist.item(existinglist.focus())['values'][0]
            mycur.execute("delete from "+tbl+" where tid='"+str(ctbd)+"'")
            convar.commit()
            existinglist.delete(existinglist.focus())
            messagebox.showinfo('Database','Teacher data Deleted')
            
    editteacherswindow=tkinter.Toplevel(homewindow)
    editteacherswindow.title('Edit Teachers')
    editteacherswindow.resizable(height=False,width=False)

    editteacherswindow.transient(homewindow)
    editteacherswindow.grab_set()
    
    top=tkinter.LabelFrame(editteacherswindow,padx=20,pady=10,bg='#1167B1')
    top.pack(fill='x',expand=True)
    headingtxt=currentdept[0][0]
    heading=tkinter.Label(top,text=headingtxt,font=("Courier",14,"bold"),bg='#1167B1',fg="#FFFFFF")
    heading.pack()
    
    bottom=tkinter.LabelFrame(editteacherswindow,padx=20,pady=20,bg='#FFD700')
    bottom.pack(fill='x',expand=True)

    lbltid=tkinter.Label(bottom,text="Teacher id",anchor='w',width=20,bg='#FFD700')
    lbltid.grid(row=0,column=0)

    lbltname=tkinter.Label(bottom,text="Teacher Name",anchor='w',width=20,bg='#FFD700')
    lbltname.grid(row=1,column=0)
    
    lbltmail=tkinter.Label(bottom,text="Email",anchor='w',width=20,bg='#FFD700')
    lbltmail.grid(row=2,column=0)

    tidtxt=tkinter.StringVar(editteacherswindow)
    tid=tkinter.Entry(bottom,textvariable=tidtxt)
    tid.grid(row=0,column=1,padx=2,ipadx=17)
    
    tnametxt=tkinter.StringVar(editteacherswindow)
    tname=tkinter.Entry(bottom,textvariable=tnametxt)
    tname.grid(row=1,column=1,padx=2,ipadx=17)
    
    tmailtxt=tkinter.StringVar(editteacherswindow)
    tmail=tkinter.Entry(bottom,textvariable=tmailtxt)
    tmail.grid(row=2,column=1,padx=2,ipadx=17)
    
    addbtn=tkinter.Button(bottom,text="ADD",command=lambda: [addteacher(tidtxt.get(),tnametxt.get(),tmailtxt.get()),
                                                             tname.delete(0,'end'),tmail.delete(0,'end'),tid.delete(0,'end'),
                                                             updatelist()],
                          relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1")
    addbtn.grid(row=3,column=1,pady=5,ipadx=17)
    
    bottommost=tkinter.LabelFrame(editteacherswindow,padx=20,pady=20,bg='#FFD700')
    bottommost.pack(fill='x',expand=True)
    

    existinglist=ttk.Treeview(bottommost)
    existinglist["columns"]=("Column 2","Column 3","Column 4")
    existinglist.column("#0",width=50,minwidth=50)
    existinglist.column("Column 2",width=150,minwidth=150)
    existinglist.column("Column 3",width=100,minwidth=100)
    existinglist.column("Column 4",width=100,minwidth=100)

    existinglist.heading("#0",text="S. no.",anchor='w')
    existinglist.heading("Column 2",text="Teacher Id",anchor='w')
    existinglist.heading("Column 3",text="Teacher Name",anchor='w')
    existinglist.heading("Column 4",text="Teacher email",anchor='w')
    tbl=currentdept[0][1]+"teachers"
    mycur.execute("show tables like '"+tbl+"'")
    dflag=mycur.fetchall()
    if(len(dflag)==1):
        mycur.execute("select * from "+tbl)
        dtable=mycur.fetchall()
    
        for i in range(0,len(dtable)):
            existinglist.insert("",i,i,text=i+1,values=dtable[i])

    existinglist.pack(fill='x')

    delbtn=tkinter.Button(bottommost,text="Delete",relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1",command=delentry)
    delbtn.pack(side='right',padx=20,pady=20)
#editteacherswindow space ends

#assignteacherswindow space starts
def assignteacherswindowcreator():
    global assignteacherswindow
    global course
    global batch
    global sem

    def updatelist():
        if(len(existinglist.size())!=0):
            for i in existinglist.get_children():
                existinglist.delete(i)
        mycur.execute("select sname,teacher from "+tempo)
        dtable=mycur.fetchall()
        for i in range(0,len(dtable)):
            existinglist.insert("",i+1,text=i+1,values=dtable[i])
            
    def updatetidlist():
        global currentdept
        global mycur
        mycur.execute("select tid from "+currentdept[0][1]+"teachers")
        temp=mycur.fetchall()
        temp2=[]
        for data in temp:
            temp2.append(data[0])
        tiddroplist["values"]=temp2
    
    def updatetnamelist():
        global currentdept
        global mycur
        mycur.execute("select tname from "+currentdept[0][1]+"teachers")
        temp=mycur.fetchall()
        temp2=[]
        for data in temp:
            temp2.append(data[0])
        tnamedroplist["values"]=temp2
    
    def updatetmaillist():
        global currentdept
        global mycur
        mycur.execute("select tmail from "+currentdept[0][1]+"teachers")
        temp=mycur.fetchall()
        temp2=[]
        for data in temp:
            temp2.append(data[0])
        tmaildroplist["values"]=temp2
        
    def updatesubnamelist():
        global currentdept
        global mycur
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()
        
        tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
        
        temp2=[]
        mycur.execute("select sname from "+tempo)
        temp=mycur.fetchall()
        
        for data in temp:
            temp2.append(data[0])
        subnamedroplist["values"]=temp2
        
    def updatesubcodelist():
        global currentdept
        global mycur
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()
        
        tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
        
        temp2=[]
        mycur.execute("select scode from "+tempo)
        temp=mycur.fetchall()
        for data in temp:
            temp2.append(data[0])
        subcodedroplist["values"]=temp2

    def approselect1(event):
        global mycur
        mycur.execute("select * from "+currentdept[0][1]+"teachers where tid='"+tidtxt.get()+"'")
        temp=mycur.fetchall()
        tnametxt.set(temp[0][1])
        tmailtxt.set(temp[0][2])
        
    def approselect2(event):
        global mycur
        mycur.execute("select * from "+currentdept[0][1]+"teachers where tname='"+tnametxt.get()+"'")
        temp=mycur.fetchall()
        tidtxt.set(temp[0][0])
        tmailtxt.set(temp[0][2])
        
    def approselect3(event):
        global mycur
        mycur.execute("select * from "+currentdept[0][1]+"teachers where tmail='"+tmailtxt.get()+"'")
        temp=mycur.fetchall()
        tidtxt.set(temp[0][0])
        tnametxt.set(temp[0][1])
    def approselect4(event):
        global currentdept
        global mycur
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()
        
        tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
        
        mycur.execute("select * from "+tempo+" where sname='"+subnametxt.get()+"'")
        temp=mycur.fetchall()
        subcodetxt.set(temp[0][1])
        
    def approselect5(event):
        global mycur
        global currentdept
        mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
        code=mycur.fetchall()
        
        tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
        
        mycur.execute("select * from "+tempo+" where scode='"+subcodetxt.get()+"'")
        temp=mycur.fetchall()
        subnametxt.set(temp[0][0])
        
    assignteacherswindow=tkinter.Toplevel(homewindow)
    assignteacherswindow.title('Assign Teachers')
    assignteacherswindow.resizable(height=False,width=False)
    assignteacherswindow.transient(homewindow)
    assignteacherswindow.grab_set()
    
    top=tkinter.LabelFrame(assignteacherswindow,padx=20,pady=10,bg="#1167B1")
    top.pack(fill='x',expand=True)
    headingtxt=course.get()+' Batch '+batch.get()+' Sem '+sem.get()
    print(headingtxt)
    heading=tkinter.Label(top,text=headingtxt,font=("Courier",14),fg="#FFFFFF",bg="#1167B1")
    heading.pack()
    
    bottom=tkinter.LabelFrame(assignteacherswindow,padx=20,pady=20,bg="#FFD700")
    bottom.pack(fill='x',expand=True)

    lbltid=tkinter.Label(bottom,text="Teacher id",anchor='w',width=20,bg="#FFD700")
    lbltid.grid(row=0,column=0)

    lbltname=tkinter.Label(bottom,text="Teacher Name",anchor='w',width=20,bg="#FFD700")
    lbltname.grid(row=1,column=0)
    
    lbltmail=tkinter.Label(bottom,text="Email",anchor='w',width=20,bg="#FFD700")
    lbltmail.grid(row=2,column=0)
    
    tidtxt=tkinter.StringVar(assignteacherswindow)
    tidoptions=["--select--"]
    tiddroplist=ttk.Combobox(bottom,textvariable=tidtxt,values=tidoptions,state="readonly",postcommand=updatetidlist)
    tiddroplist.current(0)
    tiddroplist.grid(row=0,column=1,padx=2,ipadx=17)
    tiddroplist.bind("<<ComboboxSelected>>",approselect1)
    
    tnametxt=tkinter.StringVar(assignteacherswindow)
    tnameoptions=["--select--"]
    tnamedroplist=ttk.Combobox(bottom,textvariable=tnametxt,values=tnameoptions,state="readonly",postcommand=updatetnamelist)
    tnamedroplist.current(0)
    tnamedroplist.grid(row=1,column=1,padx=2,ipadx=17)
    tnamedroplist.bind("<<ComboboxSelected>>",approselect2)
    
    tmailtxt=tkinter.StringVar(assignteacherswindow)
    tmailoptions=["--select--"]
    tmaildroplist=ttk.Combobox(bottom,textvariable=tmailtxt,values=tmailoptions,state="readonly",postcommand=updatetmaillist)
    tmaildroplist.current(0)
    tmaildroplist.grid(row=2,column=1,padx=2,ipadx=17)
    tmaildroplist.bind("<<ComboboxSelected>>",approselect3)

    lblsub=tkinter.Label(bottom,text="Subject",anchor='w',width=20,padx=10,bg="#FFD700")
    lblsub.grid(row=0,column=2)

    subnametxt=tkinter.StringVar(assignteacherswindow)
    subnameoptions=["--select--"]
    subnamedroplist=ttk.Combobox(bottom,textvariable=subnametxt,values=subnameoptions,state="readonly",postcommand=updatesubnamelist)
    subnamedroplist.current(0)
    subnamedroplist.grid(row=1,column=2,padx=2,ipadx=17)
    subnamedroplist.bind("<<ComboboxSelected>>",approselect4)

    subcodetxt=tkinter.StringVar(assignteacherswindow)
    subcodeoptions=["--select--"]
    subcodedroplist=ttk.Combobox(bottom,textvariable=subcodetxt,values=subcodeoptions,state="readonly",postcommand=updatesubcodelist)
    subcodedroplist.current(0)
    subcodedroplist.grid(row=2,column=2,padx=2,ipadx=17)
    subcodedroplist.bind("<<ComboboxSelected>>",approselect5)
    
    assignbtn=tkinter.Button(bottom,text="ASSIGN",command=lambda: [assignteacher(tidtxt.get(),subcodetxt.get()),updatelist()],
                             relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFFFFF",activeforeground="#1167B1")
    assignbtn.grid(row=3,column=1,pady=5,ipadx=17)
    
    bottommost=tkinter.LabelFrame(assignteacherswindow,padx=20,pady=20,bg="#FFD700")
    bottommost.pack(fill='x',expand=True)

    existinglist=ttk.Treeview(bottommost)
    existinglist["columns"]=("Column 2","Column 3")
    existinglist.column("#0",width=50,minwidth=50)
    existinglist.column("Column 2",width=150,minwidth=150)
    existinglist.column("Column 3",width=100,minwidth=100)

    existinglist.heading("#0",text="S. no.",anchor='w')
    existinglist.heading("Column 2",text="Subject Name",anchor='w')
    existinglist.heading("Column 3",text="Teacher Assigned",anchor='w')
    
    mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
    code=mycur.fetchall() 
    tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()+"subs"
    
    mycur.execute("show tables like '"+tempo+"'")
    dflag=mycur.fetchall()
    if(len(dflag)==1):
        mycur.execute("select * from "+tempo)
        dtable=mycur.fetchall()
        for i in range(0,len(dtable)):
            existinglist.insert("",i,i,text=i+1,values=(dtable[i][0],dtable[i][3]))

    existinglist.pack(fill='x')


#assignteacherswindow space ends

    
#createtablewindow space starts
def createtablewindowopener():
    createtablewindowcreator()
    
def createtablewindowcreator():    
    global createtablewindow
    global currentdept
    global mondayvar
    global tuesdayvar
    global wednesdayvar
    global thursdayvar
    global fridayvar
    global rnotxt

    

    mondayvar.clear()
    tuesdayvar.clear()
    wednesdayvar.clear()
    thursdayvar.clear()
    fridayvar.clear()
    def checker(atname):
                teacher=""
                global count
                mycur.execute("select * from "+atname)
                att=mycur.fetchall()
                atsub=atname+"subs"
                mycur.execute("select * from "+atsub)
                attsubs=mycur.fetchall()
                mycur.execute("select * from "+tempo)
                cttsubs=mycur.fetchall()
                for i in range(0,7):
                    print("mainloop iteration ",i)
                    for row in cttsubs:
                        print("inside monday first loop")
                        print(mondayvar[i].get())
                        if(mondayvar[i].get()!="Library"):
                            print("subject not library")
                            print("value of row[0] = ",row[0])
                            if(row[0]==mondayvar[i].get()):
                                teacher=row[3]
                                print("now teacher = ",teacher)
                        else:
                            print("found library,filling empty in teacher")
                            teacher="empty"
                    for row in attsubs:
                        print("inside monday second loop")
                        print(att[0][i],row[0])
                        if(att[0][i]==row[0]):
                            print("Monday second loop first condition satisfied")
                            print(att[0][i],row[0])
                            if(row[3]==teacher):
                                print("Teacher Found")
                                print(row[3],teacher)
                                message="Monday L"+str(i+1)+" is clashing"
                                messagebox.showinfo("Clash Detected",message)
                                return True
                            
                    for row in cttsubs:
                        print("inside tuesday first loop")
                        if(tuesdayvar[i].get()!="Library"):
                            print("subject not library")
                            print("value of row[0] = ",row[0])
                            if(row[0]==tuesdayvar[i].get()):
                                teacher=row[3]
                                print("now teacher = ",teacher)
                        else:
                            print("found library,filling empty in teacher")
                            teacher="empty"
                    for row in attsubs:
                        print("inside tuesday second loop")
                        print(att[0][i],row[0])
                        if(att[1][i]==row[0]):
                            print("Tuesday second loop first condition satisfied")
                            print(att[0][i],row[0])
                            if(row[3]==teacher):
                                print("Teacher Found")
                                print(row[3],teacher)
                                message="Tuesday L"+str(i+1)+" is clashing"
                                messagebox.showinfo("Clash Detected",message)
                                return True

                    for row in cttsubs:
                        if(wednesdayvar[i].get()!="Library"):
                            if(row[0]==wednesdayvar[i].get()):
                                teacher=row[3]
                        else:
                            teacher="empty"
                    for row in attsubs:
                        if(att[2][i]==row[0]):
                            if(row[3]==teacher):
                                message="Wednesday L"+str(i+1)+" is clashing"
                                messagebox.showinfo("Clash Detected",message)
                                return True

                    for row in cttsubs:
                        if(thursdayvar[i].get()!="Library"):
                            if(row[0]==thursdayvar[i].get()):
                                teacher=row[3]
                        else:
                            teacher="empty"
                    for row in attsubs:
                        if(att[3][i]==row[0]):
                            if(row[3]==teacher):
                                message="Thursday L"+str(i+1)+" is clashing"
                                messagebox.showinfo("Clash Detected",message)
                                return True

                    for row in cttsubs:
                        if(fridayvar[i].get()!="Library"):
                            if(row[0]==fridayvar[i].get()):
                                teacher=row[3]
                        else:
                            teacher="empty"
                    for row in attsubs:
                        if(att[4][i]==row[0]):
                            if(row[3]==teacher):
                                message="Friday L"+str(i+1)+" is clashing"
                                messagebox.showinfo("Clash Detected",message)
                                return True
                    if(i==6):
                        print("------------------------------------finished looping once--------")
                        count=count+1
                    
    def clashchecker():
        global count
        count=0
        mycur.execute("show tables")
        tables=mycur.fetchall()
        pattern="^"+currentdept[0][1]+".*[0-9]$"
        reqtabs=[]
        for tabname in tables:
            x=re.findall(pattern,tabname[0])
            if(len(x)==1 and tab!=x[0]):
                reqtabs.append(x[0])

        length=len(reqtabs)
        
        if(len(reqtabs)>0):
            global aflag
            for aname in reqtabs:
                aflag=checker(aname)
                if(aflag==True):
                    break
            if(count==length):
                addtable()
        else:
            addtable()
   
    global sflag
    createtablewindow=tkinter.Toplevel(homewindow)
    if(sflag==True):
        createtablewindow.title('TimeTable Editor (View only)')
    else:
        createtablewindow.title('TimeTable Editor')
    createtablewindow.geometry('1300x400')
    createtablewindow.resizable(height=False,width=False)
    createtablewindow.config(bg="#FFD700")
    createtablewindow.transient(homewindow)
    createtablewindow.grab_set()
    
    monday=[]
    tuesday=[]
    wednesday=[]
    thursday=[]
    friday=[]
    rnotxt=""

    headingtxt=course.get()+' Batch '+batch.get()+' Sem '+sem.get()
    heading=tkinter.Label(createtablewindow,text=headingtxt,font=("Courier",14),pady=10,fg="#FFFFFF",bg="#1167B1")
    heading.pack(side='top',fill='x')

    dx=130
    dy=100
    lblMonday=tkinter.Label(createtablewindow,text="Monday",anchor='nw',bg='#FFD700')
    lblMonday.place(x=50,y=100,height=30,width=70)
    lblTuesday=tkinter.Label(createtablewindow,text="Tuesday",anchor='nw',bg='#FFD700')
    lblTuesday.place(x=50,y=140,height=30,width=70)
    lblWednesday=tkinter.Label(createtablewindow,text="Wednesday",anchor='nw',bg='#FFD700')
    lblWednesday.place(x=50,y=180,height=30,width=70)
    lblThursday=tkinter.Label(createtablewindow,text="Thursday",anchor='nw',bg='#FFD700')
    lblThursday.place(x=50,y=220,height=30,width=70)
    lblFriday=tkinter.Label(createtablewindow,text="Friday",anchor='nw',bg='#FFD700')
    lblFriday.place(x=50,y=260,height=30,width=70)

    lbl1=tkinter.Label(createtablewindow,text="1/9am-10am",bg='#FFD700')
    lbl1.place(x=130,y=60,height=30,width=140)
    lbl2=tkinter.Label(createtablewindow,text="2/10am-11am",bg='#FFD700')
    lbl2.place(x=280,y=60,height=30,width=140)
    lbl3=tkinter.Label(createtablewindow,text="3/11am-12pm",bg='#FFD700')
    lbl3.place(x=430,y=60,height=30,width=140)
    lbl4=tkinter.Label(createtablewindow,text="4/12am-1pm",bg='#FFD700')
    lbl4.place(x=580,y=60,height=30,width=140)
    lbl5=tkinter.Label(createtablewindow,text="5/2pm-3pm",bg='#FFD700')
    lbl5.place(x=790,y=60,height=30,width=140)
    lbl6=tkinter.Label(createtablewindow,text="6/3pm-4pm",bg='#FFD700')
    lbl6.place(x=940,y=60,height=30,width=140)
    lbl7=tkinter.Label(createtablewindow,text="7/4pm-5pm",bg='#FFD700')
    lbl7.place(x=1090,y=60,height=30,width=140)

    mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
    code=mycur.fetchall()
    tab=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()
    tempo=tab+"subs"
    
    mycur.execute("select sname from "+tempo)
    temp=mycur.fetchall()
    sublist=["Library"]
    for sub in temp:
        sublist.append(sub[0])
    
    for i in range(0,7):
        mondayvar.append(tkinter.StringVar(createtablewindow))
        tuesdayvar.append(tkinter.StringVar(createtablewindow))
        wednesdayvar.append(tkinter.StringVar(createtablewindow))
        thursdayvar.append(tkinter.StringVar(createtablewindow))
        fridayvar.append(tkinter.StringVar(createtablewindow))
        
        monday.append(ttk.Combobox(createtablewindow,state='readonly',textvariable=mondayvar[i],values=sublist))
        monday[i].current(0)
        if(sflag==True):
            monday[i]['state']='disabled'
        tuesday.append(ttk.Combobox(createtablewindow,state='readonly',textvariable=tuesdayvar[i],values=sublist))
        tuesday[i].current(0)
        if(sflag==True):
            tuesday[i]['state']='disabled'
        wednesday.append(ttk.Combobox(createtablewindow,state='readonly',textvariable=wednesdayvar[i],values=sublist))
        wednesday[i].current(0)
        if(sflag==True):
            wednesday[i]['state']='disabled'
        thursday.append(ttk.Combobox(createtablewindow,state='readonly',textvariable=thursdayvar[i],values=sublist))
        thursday[i].current(0)
        if(sflag==True):
            thursday[i]['state']='disabled'
        friday.append(ttk.Combobox(createtablewindow,state='readonly',textvariable=fridayvar[i],values=sublist))
        friday[i].current(0)
        if(sflag==True):
            friday[i]['state']='disabled'
        
        monday[i].place(x=dx,y=dy)
        dy=dy+40
        tuesday[i].place(x=dx,y=dy)
        dy=dy+40
        wednesday[i].place(x=dx,y=dy)
        dy=dy+40
        thursday[i].place(x=dx,y=dy)
        dy=dy+40
        friday[i].place(x=dx,y=dy)
        dy=100
        dx=dx+150
        if(i==3):
            blbl=tkinter.Label(createtablewindow,text='B',bg='#FFD700')
            blbl.place(x=dx,y=dy,height=30,width=50)
            dy=dy+40
            rlbl=tkinter.Label(createtablewindow,text='R',bg='#FFD700')
            rlbl.place(x=dx,y=dy,height=30,width=50)
            dy=dy+40
            elbl=tkinter.Label(createtablewindow,text='E',bg='#FFD700')
            elbl.place(x=dx,y=dy,height=30,width=50)
            dy=dy+40
            albl=tkinter.Label(createtablewindow,text='A',bg='#FFD700')
            albl.place(x=dx,y=dy,height=30,width=50)
            dy=dy+40
            klbl=tkinter.Label(createtablewindow,text='K',bg='#FFD700')
            klbl.place(x=dx,y=dy,height=30,width=50)
            dx=dx+60
            dy=100


    rnolbl=tkinter.Label(createtablewindow,text="Room No.",anchor='e',bg='#FFD700')
    rnolbl.place(x=780,y=320,width=100,height=25)
    
    rnotxt=tkinter.StringVar(createtablewindow)
    rno=tkinter.Entry(createtablewindow,textvariable=rnotxt)
    if(sflag==True):
        rno['state']='disabled'
    rno.place(x=890,y=320,width=100,height=25)
    
    createbtn=tkinter.Button(createtablewindow,text="Create/Update",relief="groove",fg="#FFFFFF",bg='#1167B1',activebackground="#FFD700",activeforeground="#FFFFFF",padx=20,command=clashchecker)
    if(sflag==True):
        createbtn['state']='disabled'
    createbtn.place(x=1000,y=320,height=30,width=150)
    tvarfill(tab)
    
#createtablewindow space ends
def addtable():
    
    global currentdept
    global course
    global batch
    global sem
    global mycur
    global convar
    global rnotxt
    
    mycur.execute("select ccode from "+currentdept[0][1]+" where cname = '"+course.get()+"'")
    code=mycur.fetchall()
    tempo=currentdept[0][1]+code[0][0]+"b"+batch.get()+"s"+sem.get()

    query="insert into "+tempo+" values (%s,%s,%s,%s,%s,%s,%s)"
    records=inserter()
    if(len(records)!=0):
        table=currentdept[0][1]+"rnotable"
        
        mycur.execute("show tables like '"+tempo+"'")
        dflag=mycur.fetchall()
        if(len(dflag)==1):
            mycur.execute("truncate table "+tempo)
            convar.commit()
            mycur.executemany(query,records)
            convar.commit()
            mycur.execute("show tables like '"+table+"'")
            flag=mycur.fetchall()
            if(len(flag)==1):
                mycur.execute("select * from "+table+"")
                data=mycur.fetchall()
                if(len(data)==0):
                    mycur.execute("insert into "+table+" values('"+tempo+"','"+rnotxt.get()+"')")
                    convar.commit()
                    messagebox.showinfo("Database","TimeTable Uploaded")
                else:
                    col1=[]
                    col2=[]
                    for i in range(0,len(data)):
                        col1.append(data[i][0])
                        col2.append(data[i][1])
                    if rnotxt.get() in col2:
                        ind=col2.index(rnotxt.get())
                        if(data[ind][0]!=tempo):
                            messagebox.showinfo("Error","Room already allocated")
                        else:
                            messagebox.showinfo('Database','Data Uploaded')
                    else:
                        if(tempo in col1):
                            mycur.execute("update "+table+" set room='"+rnotxt.get()+"' where class='"+tempo+"'")
                            convar.commit()
                            messagebox.showinfo("Database","TimeTable Uploaded")
                        else:
                            mycur.execute("insert into "+table+" values('"+tempo+"','"+rnotxt.get()+"')")
                            convar.commit()
                            messagebox.showinfo("Database","TimeTable Uploaded")
            else:
                mycur.execute("create table "+table+" (class varchar(255),room varchar(255))")
                mycur.execute("insert into "+table+" values('"+tempo+"','"+rnotxt.get()+"')")
                convar.commit()
                messagebox.showinfo("Database","TimeTable Uploaded")
        else:
            mycur.execute("create table "+tempo+"(1l varchar(255),2l varchar(255),3l varchar(255),4l varchar(255),5l varchar(255),6l varchar(255),7l varchar(255))")
            convar.commit()
            mycur.executemany(query,records)
            convar.commit()
            mycur.execute("show tables like '"+table+"'")
            flag=mycur.fetchall()
            if(len(flag)==1):
                mycur.execute("select * from "+table)
                data=mycur.fetchall()
                if(len(data)==0):
                    mycur.execute("insert into "+table+" values('"+tempo+"','"+rnotxt.get()+"')")
                    convar.commit()
                    messagebox.showinfo("Database","TimeTable Uploaded")
                else:
                    col1=[]
                    col2=[]
                    
                    for i in range(0,len(data)):
                        col1.append(data[i][0])
                        col2.append(data[i][1])
                    if rnotxt.get() in col2:
                        ind=col2.index(rnotxt.get())
                        if(data[ind][0]!=tempo):
                            messagebox.showinfo("Error","Room already allocated")
                        else:
                            messagebox.showinfo('Database','Data has been uploaded')
                    else:
                        if(tempo in col1):
                            mycur.execute("update "+table+" set room='"+rnotxt.get()+"' where class='"+tempo+"'")
                            convar.commit()
                            messagebox.showinfo("Database","TimeTable Uploaded")
                        else:
                            mycur.execute("insert into "+table+" values('"+tempo+"','"+rnotxt.get()+"')")
                            messagebox.showinfo("Database","TimeTable Uploaded")
            else:
                mycur.execute("create table "+table+" (class varchar(255),room varchar(255))")
                mycur.execute("insert into "+table+" values('"+tempo+"','"+rnotxt.get()+"')")
                convar.commit()
                messagebox.showinfo("Database","TimeTable Uploaded")
def inserter():
    global mondayvar
    global tuesdayvar
    global wednesdayvar
    global thursdayvar
    global fridayvar
    global rnotxt
    record=[]
    if(len(rnotxt.get())==0):
        messagebox.showinfo("Error","Kindly fill Room no. ")
        return record
    else:
        i=0
        temp=[]
        
        for lecture in mondayvar:
            temp.append(lecture.get())
        record.append(temp)
        temp=[]
        for lecture in tuesdayvar:
            temp.append(lecture.get())
        record.append(temp)
        temp=[]
        for lecture in wednesdayvar:
            temp.append(lecture.get())
        record.append(temp)
        temp=[]
        for lecture in thursdayvar:
            temp.append(lecture.get())
        record.append(temp)
        temp=[]
        for lecture in fridayvar:
            temp.append(lecture.get())
        record.append(temp)
        return record
loginwindowopener()
tkinter.mainloop()
