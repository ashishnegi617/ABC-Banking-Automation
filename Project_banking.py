from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox    #tkinter module ke andar ek sub-module hai   #combobox is use for Drop-Down
import random                                 
import time 
import sqlite3
import gmail  # type: ignore
from tkintertable import TableCanvas, TableModel    # type: ignore
from PIL import Image,ImageTk 

win=Tk()    #creating a object of win name 
win.state('zoomed')     #for full-Screen
win.resizable(width=False,height=False)     #for blocking resizable of window 
win.configure(bg='grey')        #for background colour

title=Label(master=win,text="Banking Automation",font=('arial',40,'bold','underline'),bg='grey',fg='yellow')
title.pack(side='top',anchor='c')

date=time.strftime("%d-%B-%Y")
current_date=Label(master=win,text=date,font=('Sitka Small Semibold',14,'bold'),fg='black',bg='grey')
current_date.pack(side='top',anchor='c',pady=10)

#img=Image.open("C:/Users/ASHISH/OneDrive/Desktop/Banking Automation Project/logo.jpg").resize((260,120))
#img=Image.open("C:/Users/ASHISH/OneDrive/Desktop/github/logo.jpg").resize((260,120))
img=Image.open("logo.jpg").resize((260,120))
bitmap_img=ImageTk.PhotoImage(img,master=win)

lbl_img=Label(master=win,image=bitmap_img)
lbl_img.place(relx=0,rely=0)

footer=Label(master=win,text='By :Ashish Negi @7827273840 \n Tehri-Garhwal,Uttarakhand',font=('arial',20,'bold'),bg='grey',fg='Blue')
footer.pack(side='bottom',anchor='c')

def main_screen():
    frm=Frame(master=win)
    frm.configure(bg='silver',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    def forget_pass():      #this is like a nested function and it's not a new screen/frame it's a next frame ...
        frm.destroy()       #destroy is use for destroy old frame  
        forgetpass_screen() #it's a function 

    def login_acc():
        acn_type=cb_type.get()
        acn_no=ent_acnno.get()
        acn_pass=ent_pass.get()
        user_captcha=captcha_ent.get()
        
        if acn_type=="" and acn_no=="" and acn_pass=="":
            messagebox.showinfo("Error","Please fill the Entries")
            return                                                          #return is use for terminate the function
        
        if acn_type=='Admin' and acn_no=="0" and acn_pass=='ashish':
            if user_captcha==code_cap:
                frm.destroy()
                admin_login_screen()
            else:
                messagebox.showerror("Captcha Error","Invalid Captcha")
        elif acn_type=="User" :
            if user_captcha==code_cap :
                conobj=sqlite3.connect(database="bank.sqlite")      #connect database-->bank.sqlite
                curobj=conobj.cursor()
                curobj.execute("select * from users where users_acno=? and users_pass=?",(acn_no,acn_pass))
                tup=curobj.fetchone()       #fetch only one tuple row  because of same acc no and acn pass 
                if tup==None:
                    messagebox.showerror("Error","Acc no. and Password are Wrong")
                    return
                else:
                    global welcome_user,users_acno
                    users_acno=tup[0]
                    welcome_user=tup[1]              # tup index value is 1 because in users table users_name in Second column      
                    frm.destroy()
                    user_login_screen()
            else:
                messagebox.showerror("Captcha Error","Invalid Captcha")
        else:
            messagebox.showerror("Login Error","Invalid Acc and Password")

    lbl_acn=Label(master=frm,text="Acn Type",bg='hot pink',font=('arial',19,'bold'),width=15)
    lbl_acn.place(relx=0.15,rely=0.13)

    #ComboBox is use for Drop-Down.That's why we use ComboBox instead of Entry 
    cb_type=Combobox(master=frm,values=['----Select Acn Type----','Admin','User'],font=('arial',19,'bold'),width=19)
    cb_type.current(0)          #This is use for blinking 0 position value.
    cb_type.place(relx=0.40,rely=0.13)

    lbl_acnno=Label(master=frm,text='Acc No.',bg='gold1',font=('arial',19,'bold'),width=15)
    lbl_acnno.place(relx=0.15,rely=0.24)

    ent_acnno=Entry(master=frm,bg='white',font=('arial',19,'bold'),width=19,bd=2)
    ent_acnno.place(relx=0.40,rely=0.24)
    ent_acnno.focus()     #focus method is use for blinking the cursor which is also known as focus 

    lbl_pass=Label(master=frm,text='Password',bg='dark orange',font=('arial',19,'bold'),width=15)
    lbl_pass.place(relx=0.15,rely=0.35)

    ent_pass=Entry(master=frm,bg='white',font=('arial',19,'bold'),width=19,bd=2,show='*')   #show is use for hiding something like password
    ent_pass.place(relx=0.40,rely=0.35)

    global code_cap
    code_cap=""
    for i in range(3):
        i=chr(random.randint(65,90))
        j=str(random.randint(0,9))
        code_cap=code_cap+i+j

    global lbl_captcha
    lbl_captcha=Label(master=frm,text=f"Captcha\t\t{code_cap}",font=("arial",16,"bold"),bg="silver",bd=2,width=27,)
    lbl_captcha.place(relx=0.27,rely=0.50)
    
    def refresh():
        global lbl_captcha
        global code_cap
        code_cap=""
        for i in range(3):
            i=chr(random.randint(65,90))
            j=str(random.randint(0,9))
            code_cap=code_cap+i+j      

        lbl_captcha=Label(master=frm,text=f"Captcha\t\t{code_cap}",font=("arial",16,"bold"),bg="silver",bd=2,width=27,)
        lbl_captcha.place(relx=0.27,rely=0.50)
        
    btn_refresh=Button(master=frm,text='Refresh',font=('arial',8,'bold'),bg='violet',width=10,command=refresh)
    btn_refresh.place(relx=0.53,rely=0.51)

    captcha_fill_label=Label(master=frm,text="Enter Captcha",font=("arial",15,"bold"),width=12,bg="cornsilk2",bd=2)
    captcha_fill_label.place(relx=0.25,rely=0.59)

    captcha_ent=Entry(master=frm,font=('arial',15,'bold'),width=17,bd=2,bg="White")
    captcha_ent.place(relx=0.40,rely=0.59)

    btn_login=Button(master=frm,text='Login',font=('arial',12,'bold'),bg='lightslateblue',width=10,command=login_acc)
    btn_login.place(relx=0.40,rely=0.70)

    def reset():
        ent_acnno.delete(0,'end')
        ent_pass.delete(0,"end")
        cb_type.delete(0,"end")
        cb_type.current(0)
        ent_acnno.focus()

    btn_reset=Button(master=frm,text='Reset',font=('arial',12,'bold'),bg='lightslateblue',width=10,command=reset)
    btn_reset.place(relx=0.50,rely=0.70)

    btn_forget=Button(master=frm,text='Forget Button',font=('arial',14,'bold'),bg='spring green',width=16,command=forget_pass) #command is use for action button after click 
    btn_forget.place(relx=0.42,rely=0.79)

def forgetpass_screen():
    frm2=Frame(master=win)
    frm2.configure(highlightbackground='black',highlightthickness=2,bg='silver')
    frm2.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    forget_title=Label(master=frm2,text='Forget Password Screen',font=('arial',19,'bold'),bg='red',width=20)
    forget_title.place(relx=0.37,rely=0.05)

    def back():
        frm2.destroy()
        main_screen()

    back_button=Button(master=frm2,text='Back',width=7,font=('arial',15,'bold'),bg='brown',command=back)
    back_button.place(relx=0.0,rely=0.0)

    lbl_accno=Label(master=frm2,text="Acc No.",font=('arial',18,'bold'),width=15,bg='green',bd=2)
    lbl_accno.place(relx=0.2,rely=0.2)

    lbl_mob=Label(master=frm2,text="Mob No.",font=('arial',18,'bold'),width=15,bg='green',bd=2)
    lbl_mob.place(relx=0.2,rely=0.31)

    lbl_email=Label(master=frm2,text="Email ID",font=('arial',18,'bold'),width=15,bg='green',bd=2)
    lbl_email.place(relx=0.2,rely=0.42)

    ent_accno=Entry(master=frm2,font=('arial',18,'bold'),width=19,bg='white',bd=2)
    ent_accno.place(relx=0.4,rely=0.2)
    ent_accno.focus()

    ent_mob=Entry(master=frm2,font=('arial',18,'bold'),width=19,bg='white',bd=2)
    ent_mob.place(relx=0.4,rely=0.31)

    ent_email=Entry(master=frm2,font=('arial',18,'bold'),width=19,bg='white',bd=2)
    ent_email.place(relx=0.4,rely=0.42)
    
    def forgetpass_db():
        f_accno=ent_accno.get()
        f_email=ent_email.get()
        f_mob=ent_mob.get()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select users_pass,users_name from users where users_acno=? and users_email=? and users_mob=?",(f_accno,f_email,f_mob))
        tup=curobj.fetchone()
        
        if tup==None:
            messagebox.showerror("Forget Pass","Invalid Details")
            return
        else:
            global u_pass,u_name
            u_pass=tup[0]
            u_name=tup[1]
            otp=random.randint(1000,9999)

            try:
                con=gmail.GMail('negiashish617@gmail.com','drpo wiuz etvz adwv')
                u_text=f'''Hello {u_name} 
OTP to recover Password is {otp}
Don't share with it with anyone 

Thanks and Regard
XYZ Bank
'''
                msg=gmail.Message(to=f_email,subject="OTP for password recovery",text=u_text)
                con.send(msg)

                messagebox.showinfo('OTP for User','mail sent successfully')

                lbl_otp=Label(master=frm2,text="OTP",font=('arial',18,'bold'),bg='lightslateblue',bd=2,width=8)
                lbl_otp.place(relx=0.26,rely=0.62)

                ent_otp=Entry(master=frm2,font=('arial',18,'bold'),bd=2,bg='yellow',width=16)
                ent_otp.place(relx=0.4,rely=0.62)

                def verify_otp():
                    if otp==int(ent_otp.get()):
                        messagebox.showinfo('forget pass',f'your password is : {u_pass}')
                    else:
                        messagebox.showerror('forget pass','Invalid OTP')
                                        
                verify_btn=Button(master=frm2,text='verify',font=('arial',8,'bold'),bg='hot pink',command=verify_otp)
                verify_btn.place(relx=0.58,rely=0.63)
            except:
                messagebox.showerror('Network Problem','something went wrong with connection')

    sub_btn=Button(text='Submit',font=('arial',14,'bold'),bg='orange',width=8,command=forgetpass_db)
    sub_btn.place(relx=0.41,rely=0.55)

# This function is create for reset Button in Forget Screen
    def reset():
        ent_accno.delete(0,"end")
        ent_mob.delete(0,"end")
        ent_email.delete(0,"end")
        ent_accno.focus()

    reset_button=Button(text='Reset',font=('arial',14,'bold'),bg='orange',width=8,command=reset)
    reset_button.place(relx=0.50,rely=0.55)

def admin_login_screen():
    frm3=Frame(master=win)
    frm3.configure(highlightbackground='black',highlightthickness=2,bg='silver')
    frm3.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    def new_user():
        frm3.destroy()
        open_new_user_screen()

    def delete_user():
        frm3.destroy()
        delete_user_screen()

    def view_user():
        frm3.destroy()
        view_user_screen()

    admin_login_title=Label(master=frm3,text='Admin Home Screen',font=('arial',19,'bold'),bg='red',width=20)
    admin_login_title.place(relx=0.37,rely=0.05)

    def logout():
        frm3.destroy()
        main_screen()

    logout_button=Button(master=frm3,text='Logout',width=7,bg='brown',bd=2,font=('arial',15,'bold'),command=logout)
    logout_button.pack(side='right',anchor='n')

    open_acc_button=Button(master=frm3,text="Open User Account",font=('arial',16,'bold'),width=16,bd=2,bg='orange',command=new_user)
    open_acc_button.place(relx=0.03,rely=0.20)

    delete_user_button=Button(master=frm3,text="Delete User Account",font=('arial',16,'bold'),width=16,bd=2,bg='orange',command=delete_user)
    delete_user_button.place(relx=0.03,rely=0.30)

    view_user_button=Button(master=frm3,text="View User Account",font=('arial',16,'bold'),width=16,bd=2,bg='orange',command=view_user)
    view_user_button.place(relx=0.03,rely=0.40)

def open_new_user_screen():
    frm4=Frame(master=win)
    frm4.configure(highlightbackground='black',highlightthickness=2,bg='silver')
    frm4.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    open_new_title=Label(master=frm4,text='Open New User',font=('arial',19,'bold'),bg='orange',width=20)
    open_new_title.place(relx=0.37,rely=0.05)

    back_button=Button(master=frm4,text='Back',width=8,bg='red',font=('arial',16,'bold'),bd=2,command=admin_login_screen)
    back_button.place(relx=0.0,rely=0.0)

    def logout():
        frm4.destroy()
        main_screen()

    logout_button=Button(master=frm4,text='Logout',font=('arial',16,'bold'),bg='red',bd=2,width=8,command=logout)
    logout_button.place(relx=0.92,rely=0.0)

    name_label=Label(master=frm4,text='Name',font=('arial',20,'bold'),width=12,bd=2,bg='yellow')
    name_label.place(relx=0.25,rely=0.2)

    name_ent=Entry(master=frm4,bg='white',font=('arial',17,'bold'),width=23,bd=2)
    name_ent.place(relx=0.43,rely=0.2)
    name_ent.focus()

    mob_label=Label(master=frm4,text='Mob No.',font=('arial',20,'bold'),width=12,bd=2,bg='yellow')
    mob_label.place(relx=0.25,rely=0.32)

    mob_ent=Entry(master=frm4,bg='white',font=('arial',17,'bold'),width=23,bd=2)
    mob_ent.place(relx=0.43,rely=0.32)

    email_label=Label(master=frm4,text='Email ID.',font=('arial',20,'bold'),width=12,bd=2,bg='yellow')
    email_label.place(relx=0.25,rely=0.44)

    email_ent=Entry(master=frm4,bg='white',font=('arial',17,'bold'),width=23,bd=2)
    email_ent.place(relx=0.43,rely=0.44)

    aadhar_label=Label(master=frm4,text='Aadhar No.',font=('arial',20,'bold'),width=12,bd=2,bg='yellow')
    aadhar_label.place(relx=0.25,rely=0.56)

    aadhar_ent=Entry(master=frm4,bg='white',font=('arial',17,'bold'),width=23,bd=2)
    aadhar_ent.place(relx=0.43,rely=0.56)
        
    def new_user_db():  
        u_name=name_ent.get()           
        u_mob=mob_ent.get()
        u_email=email_ent.get()
        u_aadhar=aadhar_ent.get()
        u_bal=0
        
        u_pass=""                
        for i in range(3):
            i=chr(random.randint(65,90))
            j=str(random.randint(0,9))
            u_pass=u_pass+i+j

        conobj=sqlite3.connect(database="bank.sqlite")       
        curobj=conobj.cursor()
        curobj.execute("insert into users (users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values (?,?,?,?,?,?,?)",(u_name,u_pass,u_mob,u_email,u_bal,u_aadhar,date))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute('select max(users_acno)from users')
        u_acn=curobj.fetchone()[0]
        conobj.close()
        
        if u_name=="" and u_mob=="" and u_email=="" and u_aadhar=="":
            messagebox.showerror('Open Account',"Pls fill the details")
            return
        else:
            messagebox.showinfo('Open Account',f"Your Acno. is {u_acn} and Pass is {u_pass}")

            try:
                connection=gmail.GMail('negiashish617@gmail.com','drpo wiuz etvz adwv')
                u_text=f'''Hello {u_name}
Your Account Open Successfully in XYZ Bank 
Your Account No. is {u_acn}
Your Password is {u_pass}

Kindly change your Password when you login to app 
Don't share with your ID and Password with anyone 

Thanks and Regards
XYZ bank
'''
                msg=gmail.Message(to=u_email,subject="Account Open Successfully",text=u_text)
                connection.send(msg)
                messagebox.showinfo("New user","Mail sent Successfully")
            except:             
                messagebox.showerror("Network Problem","Something went wrong with connection")

    submit_button=Button(master=frm4,text='Submit',font=('arial',15,'bold'),bg='brown',bd=2,width=7,command=new_user_db)
    submit_button.place(relx=0.38,rely=0.68)

    def reset():
        name_ent.delete(0,"end")
        mob_ent.delete(0,"end")
        email_ent.delete(0,"end")
        aadhar_ent.delete(0,"end")
        name_ent.focus()

    reset_button=Button(master=frm4,text='Reset',font=('arial',15,'bold'),bg='brown',bd=2,width=7,command=reset)
    reset_button.place(relx=0.47,rely=0.68)

def delete_user_screen():
    frm5=Frame(master=win)
    frm5.configure(highlightbackground='black',highlightthickness=2,bg='silver')
    frm5.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    open_new_title=Label(master=frm5,text='Delete User Account',font=('arial',19,'bold'),bg='orange',width=20)
    open_new_title.place(relx=0.37,rely=0.05)

    back_button=Button(master=frm5,text='Back',width=8,bg='red',font=('arial',16,'bold'),bd=2,command=admin_login_screen)
    back_button.place(relx=0.0,rely=0.0)

    def logout():
        frm5.destroy()
        main_screen()

    logout_button=Button(master=frm5,text='Logout',font=('arial',16,'bold'),bg='red',bd=2,width=8,command=logout)
    logout_button.place(relx=0.92,rely=0.0)

    acn_label=Label(master=frm5,text='Account No.',font=('arial',20,'bold'),bg='yellow',bd=2,width=12)
    acn_label.place(relx=0.25,rely=0.25)

    acn_ent=Entry(master=frm5,font=('arial',20,'bold'),width=19,bd=2,bg='white')
    acn_ent.place(relx=0.42,rely=0.25)
    acn_ent.focus()

    aadhar_label=Label(master=frm5,text='Aadhar No.',font=('arial',20,'bold'),bg='yellow',bd=2,width=12)
    aadhar_label.place(relx=0.25,rely=0.36)

    aadhar_ent=Entry(master=frm5,font=('arial',20,'bold'),width=19,bd=2,bg='white')
    aadhar_ent.place(relx=0.42,rely=0.36)
    
    def delete_user_db():
        uacn=acn_ent.get()
        uadhar=aadhar_ent.get()
        if uacn=="" or uadhar=="":
            messagebox.showerror("Delete User","Pls fill the details")
            return
        else:
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_email from users where users_acno=? and users_adhar=?",(uacn,uadhar))
            u_email=curobj.fetchone()
            if u_email==None:
                messagebox.showerror("Delete User","User not found error")
                return
            else:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("delete from users where users_acno=? and users_adhar=?",(uacn,uadhar))
                curobj.execute("delete from txn where txn_acno=?",(uacn,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Delete User","User Account deleted successfully")
                try:
                    connection=gmail.GMail('negiashish617@gmail.com','drpo wiuz etvz adwv')
                    u_text=f'''Hello {u_name}
Your Account Delete Successfully in XYZ Bank 
Your Account No. is {uacn}

Thanks and Regards
XYZ bank
'''
                    msg=gmail.Message(to=u_email,subject="Account Open Successfully",text=u_text)
                    connection.send(msg)
                    messagebox.showinfo("Delete User","Mail sent Successfully")
                except:             
                    messagebox.showerror("Network Problem","Something went wrong with connection")
        
    delete_button=Button(master=frm5,text='Delete',font=('arial',14,'bold'),bg='red',bd=2,width=9,command=delete_user_db)
    delete_button.place(relx=0.38,rely=0.48)

    def reset():
        acn_ent.delete(0,"end")
        aadhar_ent.delete(0,"end")
        acn_ent.focus()

    reset_button=Button(master=frm5,text='Reset',font=('arial',14,'bold'),bg='red',width=9,command=reset)
    reset_button.place(relx=0.48,rely=0.48)

def view_user_screen():
    frm6=Frame(master=win)
    frm6.configure(highlightbackground='black',highlightthickness=2,bg='silver')
    frm6.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    open_new_title=Label(master=frm6,text='View User Account',font=('arial',19,'bold'),bg='orange',width=20)
    open_new_title.place(relx=0.37,rely=0.05)

    back_button=Button(master=frm6,text='Back',width=8,bg='red',font=('arial',16,'bold'),bd=2,command=admin_login_screen)
    back_button.place(relx=0.0,rely=0.0)

    def logout():
        frm6.destroy()
        main_screen()

    logout_button=Button(master=frm6,text='Logout',font=('arial',16,'bold'),bg='red',bd=2,width=8,command=logout)
    logout_button.place(relx=0.92,rely=0.0)

    acn_label=Label(master=frm6,text="Account No.",font=('arial',19,'bold'),bg='yellow',width=15,bd=2)
    acn_label.place(relx=0.30,rely=0.20)

    acn_ent=Entry(master=frm6,font=('arial',19,'bold'),bd=2)
    acn_ent.place(relx=0.48,rely=0.20)
    acn_ent.focus()

    def view_user_db():
        uacn=acn_ent.get()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acno=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        if tup==None:
            messagebox.showerror("View User","Account Doesn't Exist")
        else:
            name_label=Label(master=frm6,text="Name",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
            name_label.place(relx=0.03,rely=0.36)

            name_ent=Entry(master=frm6,font=('arial',17,'bold'),width=19,bg="White",bd=2)
            name_ent.place(relx=0.19,rely=0.36)

            aadhar_label=Label(master=frm6,text="Aadhar No.",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
            aadhar_label.place(relx=0.50,rely=0.36)

            aadhar_ent=Entry(master=frm6,font=('arial',17,'bold'),width=19,bg="White",bd=2)
            aadhar_ent.place(relx=0.66,rely=0.36)

            mob_label=Label(master=frm6,text="Mob No.",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
            mob_label.place(relx=0.03,rely=0.49)

            mob_ent=Entry(master=frm6,font=('arial',17,'bold'),width=19,bg="White",bd=2)
            mob_ent.place(relx=0.19,rely=0.49)

            email_label=Label(master=frm6,text="Email Id",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
            email_label.place(relx=0.50,rely=0.49)

            email_ent=Entry(master=frm6,font=('arial',17,'bold'),width=19,bg="White",bd=2)
            email_ent.place(relx=0.66,rely=0.49)

            open_date_label=Label(master=frm6,text="Opening Date",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
            open_date_label.place(relx=0.03,rely=0.62)

            open_date_ent=Entry(master=frm6,font=('arial',17,'bold'),width=19,bg="White",bd=2)
            open_date_ent.place(relx=0.19,rely=0.62)

            balance_label=Label(master=frm6,text="Balance",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
            balance_label.place(relx=0.50,rely=0.62)

            balance_ent=Entry(master=frm6,font=('arial',17,'bold'),width=19,bg="White",bd=2)
            balance_ent.place(relx=0.66,rely=0.62)

        name_ent.insert(0,tup[1])
        aadhar_ent.insert(0,tup[6])
        mob_ent.insert(0,tup[3])
        email_ent.insert(0,tup[4])
        open_date_ent.insert(0,tup[7])
        balance_ent.insert(0,tup[5])

    submit_button=Button(master=frm6,text="Search",font=('arial',9,'bold'),width=7,bd=2,bg="grey",command=view_user_db)
    submit_button.place(relx=0.71,rely=0.21)

def user_login_screen():
    frm7=Frame(master=win)
    frm7.configure(highlightbackground='black',highlightthickness=2,bg='silver')
    frm7.place(relx=0.0,rely=0.15,relheight=0.75,relwidth=1)

    screen_title="User Home Screen"     # 1.1 screen title 
    frm_title=Label(master=frm7,text=screen_title,font=('arial',17,'bold'),width=19,bg="orange",bd=2)
    frm_title.place(relx=0.37,rely=0.05)

    welcome_title=Label(master=frm7,text=f'Welcome {welcome_user}',font=('arial',15,'bold'),width=20,bg='yellow',bd=2)
    welcome_title.pack(side='top',anchor='w')

    def logout():
        frm7.destroy()
        main_screen()

    logout_button=Button(master=frm7,text="Logout",font=('arial',14,'bold'),width=10,bd=2,bg='red',command=logout)
    logout_button.place(relx=0.91,rely=0.0)

    def user_detail_screen():        # 1.2 screen title  
        screen_title="User Details Screen"
        frm_title.configure(text=screen_title)      #place and items all will be the same if we don't configure 
         
        inner_frm=Frame(master=frm7,highlightbackground='black',highlightthickness=2,bg='darkgray')
        inner_frm.place(relx=0.25,rely=0.17,relheight=0.67,relwidth=0.60)

        def back():
            inner_frm.destroy()
            user_login_screen()

        back_button=Button(master=inner_frm,text="Back",font=("arial",14,"bold"),width=10,bg="cyan",command=back)
        back_button.pack(side="top",anchor="e")     

        name_label=Label(master=inner_frm,text="Name",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
        name_label.place(relx=0.03,rely=0.10)

        name_ent=Entry(master=inner_frm,font=('arial',17,'bold'),width=17,bg="White",bd=2)
        name_ent.place(relx=0.29,rely=0.10)

        aadhar_label=Label(master=inner_frm,text="Aadhar No.",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
        aadhar_label.place(relx=0.03,rely=0.23)

        aadhar_ent=Entry(master=inner_frm,font=('arial',17,'bold'),width=17,bg="White",bd=2)
        aadhar_ent.place(relx=0.29,rely=0.23)

        mob_label=Label(master=inner_frm,text="Mob No.",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
        mob_label.place(relx=0.03,rely=0.36)

        mob_ent=Entry(master=inner_frm,font=('arial',17,'bold'),width=17,bg="White",bd=2)
        mob_ent.place(relx=0.29,rely=0.36)

        email_label=Label(master=inner_frm,text="Email Id",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
        email_label.place(relx=0.03,rely=0.49)

        email_ent=Entry(master=inner_frm,font=('arial',17,'bold'),width=17,bg="White",bd=2)
        email_ent.place(relx=0.29,rely=0.49)

        open_date_label=Label(master=inner_frm,text="Opening Date",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
        open_date_label.place(relx=0.03,rely=0.62)

        open_date_ent=Entry(master=inner_frm,font=('arial',17,'bold'),width=17,bg="White",bd=2)
        open_date_ent.place(relx=0.29,rely=0.62)

        balance_label=Label(master=inner_frm,text="Balance",font=('arial',17,'bold'),width=12,bd=2,bg='red',fg='yellow')
        balance_label.place(relx=0.03,rely=0.75)

        balance_ent=Entry(master=inner_frm,font=('arial',17,'bold'),width=17,bg="White",bd=2)
        balance_ent.place(relx=0.29,rely=0.75)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acno=?",(users_acno,))
        tup=curobj.fetchone()
        conobj.close()

        name_ent.insert(0,tup[1])
        aadhar_ent.insert(0,tup[6])
        mob_ent.insert(0,tup[3])
        email_ent.insert(0,tup[4])
        open_date_ent.insert(0,tup[7])
        balance_ent.insert(0,tup[5])

    check_detail_button=Button(master=frm7,text="Check Details",font=('arial',16,'bold'),bd=2,bg='violet',width=16,command=user_detail_screen)
    check_detail_button.place(relx=0.00,rely=0.25)

    def user_deposit_screen():       #1.3 screen title
        screen_title="User Deposit Screen"
        frm_title.configure(text=screen_title)
        
        inner_frm=Frame(master=frm7,highlightbackground='black',highlightthickness=2,bd=2,bg='darkgray')
        inner_frm.place(relx=0.25,rely=0.17,relheight=0.67,relwidth=0.60)

        def back():
            inner_frm.destroy()
            user_login_screen()

        back_button=Button(master=inner_frm,text="Back",font=("arial",14,"bold"),width=10,bg="cyan",command=back)
        back_button.pack(side="top",anchor="e")
        
        amt_label=Label(master=inner_frm,text="Amount",font=("arial",19,"bold"),bg="red",fg="yellow",bd=2,width=11)
        amt_label.place(relx=0.11,rely=0.20)

        amt_ent=Entry(master=inner_frm,font=("arial",19,"bold"),bd=1,bg="white",width=19)
        amt_ent.place(relx=0.36,rely=0.20)
        amt_ent.focus()
        
        def deposit():
            uamt=int(amt_ent.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,users_acno))   
            conobj.commit()
            conobj.close()
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_bal from users where users_acno=?",(users_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            messagebox.showinfo('Deposit',f"Amt Deposit {uamt} and Updated Bal is {ubal}")

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("insert into txn (txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)",(users_acno,"Cr",uamt,ubal,date))
            conobj.commit()
            conobj.close()

        sumbit_button=Button(master=inner_frm,text="Submit",font=("arial",10,"bold"),bg="gray",bd=2,width=8,command=deposit)
        sumbit_button.place(relx=0.38,rely=0.36)
        
    deposit_button=Button(master=frm7,text="Deposit",font=('arial',16,'bold'),bd=2,bg='light blue',width=16,command=user_deposit_screen)
    deposit_button.place(relx=0.00,rely=0.35)

    def user_withdraw_screen():       #1.4 screen title
        screen_title="User Withdraw Screen"
        frm_title.configure(text=screen_title)

        inner_frm=Frame(master=frm7,highlightbackground='black',highlightthickness=2,bg='darkgray')
        inner_frm.place(relx=0.25,rely=0.17,relheight=0.67,relwidth=0.60)

        def back():
            inner_frm.destroy()
            user_login_screen()

        back_button=Button(master=inner_frm,text="Back",font=("arial",14,"bold"),width=10,bg="cyan",command=back)
        back_button.pack(side="top",anchor="e")

        amt_label=Label(master=inner_frm,text="Amount",font=("arial",19,"bold"),bg="red",fg="yellow",bd=2,width=11)
        amt_label.place(relx=0.11,rely=0.20)

        amt_ent=Entry(master=inner_frm,font=("arial",19,"bold"),bd=1,bg="white",width=19)
        amt_ent.place(relx=0.36,rely=0.20)
        amt_ent.focus()

        def withdraw():        
            uamt=int(amt_ent.get())

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_bal from users where users_acno=?",(users_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal<uamt :
                messagebox.showerror('withdraw',"Insufficient Balance")
                return
            else:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,users_acno))   
                conobj.commit()
                conobj.close()

            messagebox.showinfo('Withdraw',f"Amt Withdraw {uamt} and Updated Bal is {ubal-uamt}")

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("insert into txn (txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)",(users_acno,"Dr",uamt,ubal-uamt,date))
            conobj.commit()
            conobj.close()

        sumbit_button=Button(master=inner_frm,text="Submit",font=("arial",10,"bold"),bg="gray",bd=2,width=8,command=withdraw)
        sumbit_button.place(relx=0.38,rely=0.36)

    withdraw_button=Button(master=frm7,text="Withdraw",font=('arial',16,'bold'),bd=2,bg='light green',width=16,command=user_withdraw_screen)
    withdraw_button.place(relx=0.00,rely=0.45)

    def user_update_screen():       #1.5 screen title
        screen_title="User Update Screen"
        frm_title.configure(text=screen_title)  

        inner_frm=Frame(master=frm7,highlightbackground='black',highlightthickness=2,bg='darkgray')
        inner_frm.place(relx=0.25,rely=0.17,relheight=0.67,relwidth=0.60)

        def back():
            inner_frm.destroy()
            user_login_screen()

        back_button=Button(master=inner_frm,text="Back",font=("arial",14,"bold"),width=10,bg="cyan",command=back)
        back_button.pack(side="top",anchor="e")  

        pass_label=Label(master=inner_frm,text="Password",font=("arial",17,"bold"),width=14,bg="red",fg="yellow")
        pass_label.place(relx=0.12,rely=0.22)

        pass_ent=Entry(master=inner_frm,font=("arial",17,"bold"),width=19,bg="white",bd=2)
        pass_ent.place(relx=0.40,rely=0.22)
        pass_ent.focus()

        mob_label=Label(master=inner_frm,text="Mobile No.",font=("arial",17,"bold"),fg="yellow",bg="red",width=14)
        mob_label.place(relx=0.12,rely=0.35)

        mob_ent=Entry(master=inner_frm,font=("arial",17,"bold"),width=19,bg="white",bd=2)
        mob_ent.place(relx=0.40,rely=0.35)

        email_label=Label(master=inner_frm,text="Email ID",font=("arial",17,"bold"),fg="yellow",bg="red",width=14)
        email_label.place(relx=0.12,rely=0.48)

        email_ent=Entry(master=inner_frm,font=("arial",17,"bold"),width=19,bg="white",bd=2)
        email_ent.place(relx=0.40,rely=0.48)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select users_pass,users_mob,users_email from users where users_acno=?",(users_acno,))
        tup=curobj.fetchone()
        conobj.close()

        pass_ent.insert(0,tup[0])       #insert method is use for inserting the data into entry 
        mob_ent.insert(0,tup[1])
        email_ent.insert(0,tup[2])

        def update_db():
            upass=pass_ent.get()
            umob=mob_ent.get()
            uemail=email_ent.get()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update users set users_pass=?, users_mob=?, users_email=? where users_acno=?",(upass,umob,uemail,users_acno))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","Update Successfully")

        submit_button=Button(master=inner_frm,text="Submit",font=("arial",10,"bold"),bg="gray",bd=2,width=8,command=update_db)
        submit_button.place(relx=0.37,rely=0.62)

    update_button=Button(master=frm7,text="Update",font=('arial',16,'bold'),bd=2,bg='yellow',width=16,command=user_update_screen)
    update_button.place(relx=0.00,rely=0.55)

    def user_transfer_screen():       #1.6 screen title
        screen_title="User Transfer Screen"
        frm_title.configure(text=screen_title)

        inner_frm=Frame(master=frm7,highlightbackground='black',highlightthickness=2,bg='darkgray')
        inner_frm.place(relx=0.25,rely=0.17,relheight=0.67,relwidth=0.60)

        def back():
            inner_frm.destroy()
            user_login_screen()

        back_button=Button(master=inner_frm,text="Back",font=("arial",14,"bold"),width=10,bg="cyan",command=back)
        back_button.pack(side="top",anchor="e")

        to_label=Label(master=inner_frm,text="To Account No.",font=("arial",18,"bold"),fg="yellow",bg="red",width=14,bd=2)
        to_label.place(relx=0.12,rely=0.20)

        to_ent=Entry(master=inner_frm,font=('arial',18,'bold'),bg="white",bd=2)
        to_ent.place(relx=0.42,rely=0.20)

        amt_label=Label(master=inner_frm,text="Amount.",font=("arial",18,"bold"),fg="yellow",bg="red",width=14,bd=2)
        amt_label.place(relx=0.12,rely=0.33)

        amt_ent=Entry(master=inner_frm,font=('arial',18,'bold'),bg="white",bd=2)
        amt_ent.place(relx=0.42,rely=0.33)

        def transfer():
            utoacn=int(to_ent.get())
            uamt=int(amt_ent.get())

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from users where users_acno=?",(utoacn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None or utoacn==users_acno:
                messagebox.showerror('Transfer','Invalid Acn No.')
                return                     
            else:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select users_bal from users where users_acno=?",(users_acno,))
                ubal=curobj.fetchone()[0]
                conobj.close()
                if uamt>ubal:
                    messagebox.showinfo("Transfer","Insufficient Balance")
                    return
                else:
                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("Update users set users_bal=users_bal+? where users_acno=?",(uamt,utoacn))
                    curobj.execute("Update users set users_bal=users_bal-? where users_acno=?",(uamt,users_acno))
                    conobj.commit()
                    conobj.close()

                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("Insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)",(utoacn,"Cr",uamt,ubal+uamt,date))
                    curobj.execute("Insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)",(users_acno,"Dr",uamt,ubal-uamt,date))
                    conobj.commit()
                    conobj.close()

                    messagebox.showinfo("Transfer",f"{uamt} transfer and Balance is {ubal-uamt}")

        submit_button=Button(master=inner_frm,text="Submit",font=("arial",10,"bold"),width=8,bg="gray",bd=2,command=transfer)
        submit_button.place(relx=0.40,rely=0.46)

    transfer_button=Button(master=frm7,text="Transfer",font=('arial',16,'bold'),bd=2,bg='orange',width=16,command=user_transfer_screen)
    transfer_button.place(relx=0.00,rely=0.65)

    def user_transaction_his_screen():       #1.7 screen title
        screen_title="User Txn history Screen"
        frm_title.configure(text=screen_title)

        inner_frm=Frame(master=frm7,highlightbackground='black',highlightthickness=2,bg='silver')
        inner_frm.place(relx=0.25,rely=0.17,relheight=0.67,relwidth=0.60)

        def back():
            inner_frm.destroy()
            user_login_screen()

        back_button=Button(master=inner_frm,text="Back",font=("arial",14,"bold"),width=10,bg="cyan",command=back)
        back_button.pack(side="top",anchor="e")

        data={}
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from txn where txn_acno=?",(users_acno,))
        tups=curobj.fetchall()

        i=1
        for tup in tups:
            data[str(i)]={'Txn Amt':tup[3],'Txn Type':tup[2],'Updated Bal':tup[4],'Txn Date':tup[5],'txn ID':tup[0]}
            i+=1
        model=TableModel()
        model.importDict(data)

        table_frm=Frame(master=inner_frm)
        table_frm.place(relx=0.0,rely=0.0)
        table=TableCanvas(table_frm,model=model,editable=False)
        table.show()

    transaction_history_button=Button(master=frm7,text="Transaction History",font=('arial',16,'bold'),bd=2,bg='gray',width=16,command=user_transaction_his_screen)
    transaction_history_button.place(relx=0.00,rely=0.75)

main_screen()

win.mainloop()


