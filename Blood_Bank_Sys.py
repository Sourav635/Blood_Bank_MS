from tkinter import *
import csv
from collections import Counter
from PIL import ImageTk, Image
from tkinter import messagebox
import time
from datetime import *
from tkcalendar import Calendar
import os
import demo
import re

cwd = os.getcwd()

# Class for All Widgets like --> Label, Button, Entry
class Widgets():

    def tag(self, screen, text, bd, row=None, column=None, columnspan=0, rowspan=0, bg=None, padx=5, pady=5, font="Ubuntu 14 bold", sticky=None):
        Label(screen, text=text, bd=bd, font=font, bg=bg, pady=pady, padx=padx).grid(
            row=row, column=column)

    def entry(self, screen, bd, textvariable, row, column, padx=5, pady=5):
        return Entry(screen, bd=bd, textvariable=textvariable).grid(
            row=row, column=column)

    def rb(self, screen, bd, variable, value, text, row, column, font="Ubuntu 14", bg="white", padx=5, pady=5):
        return Radiobutton(screen, bd=bd, variable=variable, value=value,
                           text=text, font=font, bg=bg, padx=padx, pady=pady).grid(row=row, column=column)

    def btn(self, screen, text, command, bd, row, column, font="Ubuntu 14", bg="grey", padx=10, pady=1, columnspan=1):
        return Button(screen, text=text, command=command, bd=bd, padx=padx, pady=pady,
                      font="Ubuntu 14", bg=bg).grid(row=row, column=column, columnspan=columnspan)

    def nl(self, row, column=5):
        Label().grid(row=row, column=column)


w = Widgets()                   # Instantiating Widegets Class


class Main(Widgets):            # Main Class containing all function and Windows

    def msgs(self):
        self.scr.destroy()
        messagebox.showinfo(
            "Information", "Your Data Has been stored\tThanks for Donating !!!")

    def msgs2(self):
        self.req_scr.destroy()
        messagebox.showinfo(
            "Information", "Your Request Has been submitted\n\nWill Contact you soon!!!")

    def quit(self, master):
        res = messagebox.askyesno(
            'Close App', 'Do you want to close application?', parent=master)
        if res == True:
            master.destroy()
        else:
            pass

    def vaidation_error(self, master, name="", mob="", age="", city="",):
        pass
        # messagebox.showwarning(name+mob+age+city,parent=master)

    def validation(self):

        # --> Name Vaildation
        fname = self.fname.get()
        fname = fname.strip()

        lname = self.lname.get()
        lname = lname.strip()

        pattern = re.compile(r"[A-Za-z]+")
        try:
            if pattern.match(fname + lname).group() == (fname + lname):
                name_valid = True
            else:
                messagebox.showwarning(
                    "Warning", "Enter Name Properly", parent=self.scr)
                name_valid = False
                self.fname.set("")
                self.lname.set("")

        except:
            messagebox.showwarning(
                "Warning", "Enter Name Properly", parent=self.scr)
            name_valid = False
            self.fname.set("")
            self.lname.set("")

        # --> Mobile Number Validation

        pattern = re.compile(r"(\+91\s?)?(0\s?)?\d{10}")

        try:
            if pattern.match(self.mob.get()).group() == self.mob.get():
                mob_valid = True
            else:
                messagebox.showwarning(
                    "Warning", "Enter Mobile Number Properly", parent=self.scr)
                self.mob.set("")
                mob_valid = False
        except:
            messagebox.showwarning(
                "Warning", "Enter Mobile Number Properly", parent=self.scr)
            self.mob.set("")
            mob_valid = False

        # --> City Validation
        city = self.city.get()
        city = city.strip()

        pattern = re.compile(r"[A-Za-z]+")
        try:
            if pattern.match(city).group() == city:
                city_valid = True
            else:
                messagebox.showwarning(
                    "Warning", "Enter City Properly", parent=self.scr)
                self.city.set("")
                city_valid = False
        except:
            messagebox.showwarning(
                "Warning", "Enter City Properly", parent=self.scr)
            self.city.set("")
            city_valid = False

        # --> Date Validation

        if self.inspection == True:
            date_str = self.cal.get_date()
        else:
            date_str = self.today
        date_format = "%m/%d/%y"
        date_obj = datetime.strptime(date_str, date_format).date()
        if date_obj > datetime.now().date():
            date_valid = True
        else:
            messagebox.showerror(
                "Warning", "Choose Date correctly !!!", parent=self.scr)
            date_valid = False

        if all([name_valid, mob_valid, city_valid, date_valid]):
            self.store()

    def req_form_validation(self):

        # --> Name Validation
        p_name = self.p_name.get()

        pattern = re.compile(r"[A-Za-z]+\s*[A-Za-z]*")
        try:
            if pattern.match(p_name).group() == (p_name):
                p_name_valid = True
            else:
                messagebox.showwarning(
                    "Warning", "Enter Name properly !!!", parent=self.req_scr)
                p_name_valid = False
                self.p_name.set("")
        except:
            messagebox.showwarning(
                "Warning", "Enter Name properly !!!", parent=self.req_scr)
            p_name_valid = False
            self.p_name.set("")

        # --> Age
        age = self.p_age.get()
        pattern = re.compile(r"[1-9]\d")

        try:
            if pattern.match(age).group() == age:
                p_age_valid = True
            else:
                messagebox.showwarning(
                    "Warning", "Enter Age Properly", parent=self.req_scr)
                self.p_age.set("")
                p_age_valid = False
        except:
            messagebox.showwarning(
                "Warning", "Enter Age Properly", parent=self.req_scr)
            self.p_age.set("")
            p_age_valid = False

        # --> Mobile validation

        pattern = re.compile(r"(\+91\s?)?(0\s?)?\d{10}")
        try:
            if pattern.match(self.p_mob.get()).group() == self.p_mob.get():
                mob_valid = True
            else:
                messagebox.showwarning(
                    "Warning", "Enter Mobile Number Properly", parent=self.req_scr)
                self.p_mob.set("")
                mob_valid = False
        except:
            messagebox.showwarning(
                "Warning", "Enter Mobile Number Properly", parent=self.req_scr)
            self.p_mob.set("")
            mob_valid = False

        if all([p_name_valid, p_age_valid, mob_valid]):
            self.msgs2()
            self.req_store()

    def req_store(self):

        p_name = self.p_name.get()
        p_age = int(self.p_age.get())
        sickness = []
        l = [self.chk_btn1.get(), self.chk_btn2.get(),
             self.chk_btn3.get(), self.chk_btn4.get()]
        d_list = ["Diabetes", "High BP", "Anemia", "Hemophilia"]
        for x in range(4):
            if l[x]:
                sickness.append(d_list[x])
        p_mob = self.p_mob.get()
        p_blood_grp = self.p_blood_grp.get()

        demo.store_data_reqform(p_name, p_blood_grp,
                                p_age, str(sickness), p_mob)

        with open("Req_form.csv", "a", newline="") as rform:
            writer = csv.writer(rform)
            writer.writerow([p_name, p_age, p_blood_grp, sickness, p_mob])

    def store(self):            # Store Donor Data to Data.csv

        demo.insertdata(
            self.fname.get(),
            self.lname.get(),
            self.gender.get(),
            self.blood_grp_char.get() + self.blood_grp_sign.get(),
            self.mob.get(),
            self.city.get(),
            self.cal.get_date()
        )
        _fname = self.fname.get()
        _lname = self.lname.get()
        _gender = self.gender.get()

        if _gender == 1:
            _gender = "Male"
        elif _gender == 2:
            _gender = "Female"

        _blood_grp_char = self.blood_grp_char.get()
        _blood_grp_sign = self.blood_grp_sign.get()
        _bg = _blood_grp_char + _blood_grp_sign

        _mob = self.mob.get()

        _city = self.city.get()
        _date = self.cal.get_date()
        # print("Fname:", _fname, "Lname:", _lname, "Gender:",
        #       _gender, "Bg:", _bg, "Mobile:", _mob, "City:", _city, "Date:", _date)

        with open("Data.csv", "a", newline="") as d:        # Writing in csv
            d_writer = csv.writer(d)
            d_writer.writerow(
                [_fname, _lname, _gender, _bg, _mob, _city, _date])

        self.read_data()                # Calling Function to read data

        with open("blood_bank_status.csv", "r") as b_:
            reader = csv.reader(b_)
            updated_data = []
            for x in reader:
                if x[1] == _bg:
                    updated_data.append([x[0], x[1] + 1])
                else:
                    updated_data.append(x)

        with open("blood_bank_status.csv", "w", newline="") as bb_:
            writer = csv.writer(bb_)
            for x in updated_data:
                writer.writerow(x)
        self.msgs()

    def read_data(self):              # Read Data Of Donors

        with open("data.csv", "r") as d_:
            reader = csv.reader(d_)
            blood_grp_units = []
            for x in reader:
                blood_grp_units.append(x[3])
        with open("blood_bank_status.csv", "w", newline="") as b_:
            writer = csv.writer(b_)
            a = Counter(blood_grp_units)
            for x in a:
                writer.writerow([x, a[x]])

    def reset(self):                            # Reset all Entries
        self.fname.set("")
        self.lname.set("")
        self.gender.set(0)
        self.blood_grp_char.set("A")
        self.blood_grp_sign.set("+")
        self.mob.set("")
        self.city.set("")

    def chk(self):                      # Check whether User is Donor or Receiver

        if self.status.get() == "Donor":
            self.donor()
        else:
            self.receiver()

    # --> Creating Calendar

    def cal(self):

        self.win = Toplevel(self.scr)
        self.win.geometry("310x230+1015+380")
        self.win.title("Calendar")
        self.win.iconbitmap(cwd + r"\Blood.ico")
        self.win.config(bg="khaki")

        self.cal = Calendar(self.win, selectmode="day",
                            year=2021, month=6, day=1)
        self.cal.pack()
        select_date_btn = Button(
            self.win, text="Select Date", command=self.store_date, bd=5)
        select_date_btn.pack()
        self.win.mainloop()

    def store_date(self):
        self.win.destroy()
        self.inspection = True
        self.selected_date.config(text=self.cal.get_date())

    # --> Donor Window
    def donor(self):

        self.inspection = False
        # --> self.scretup
        self.scr = Toplevel(self.home)
        self.scr.attributes("-topmost", 1)
        self.scr.iconbitmap(cwd + r"\Blood.ico")
        self.scr.title("Blood Bank System")
        self.scr.config(bg="silver")
        self.scr.geometry("760x510+250+100")
        self.scr.option_add("*Font", "Ubuntu")
        self.scr.resizable(width=False, height=False)

        # --> Background Setup using Canvas
        canvas = Canvas(self.scr, width=800, height=500)
        image = ImageTk.PhotoImage(Image.open(cwd + r"\img4.jpg"))
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.grid(row=0, column=0, rowspan=20, columnspan=20)

        # --> Row_width Configuration
        for x in range(12):
            self.scr.grid_rowconfigure(x, minsize=20)
        self.scr.grid_rowconfigure(14, minsize=100)

        self.fname = StringVar()                       # Creating Instance Variables
        self.lname = StringVar()
        self.gender = IntVar()
        self.mob = StringVar()
        self.city = StringVar()

        heading = Label(self.scr, text="Donor Registration Form", font="Ubuntu 14 bold underline", bg="Silver", width="65").grid(
            row=0, column=0, columnspan=5)

        # --> First Name Label And Entry
        First_Name_Tag = self.tag(self.scr, "First Name", 5, 2, 0)
        First_Name_Entry = Entry(
            self.scr, textvariable=self.fname, bd=5).grid(row=2, column=1)

        # --> Last Name Label And Entry
        Last_Name_Tag = self.tag(self.scr, "Last Name", 5, 2, 2)
        Last_Name_Entry = self.entry(self.scr, 5, self.lname, 2, 3)
        self.nl(3)

        # --> Gender Label And RadioButtons
        Gender_Tag = self.tag(self.scr, "Gender", 5, 4, 0)
        Gender_RB1 = self.rb(self.scr, 5, self.gender, 1, "Male", 4, 1)
        Gender_RB2 = self.rb(self.scr, 5, self.gender, 2, "Female", 4, 2)
        self.nl(5)

        # --> Blood Group Label And OptionMenu
        self.blood_grp_char = StringVar()
        self.blood_grp_sign = StringVar()
        self.blood_grp_char.set("A")
        self.blood_grp_sign.set("+")

        Blood_Group_Label = self.tag(self.scr, "Blood Group", 5, 6, 0)
        Blood_Group_char_Option_Menu = OptionMenu(
            self.scr, self.blood_grp_char, "A", "B", "AB", "O")
        Blood_Group_char_Option_Menu.grid(row=6, column=1)
        Blood_Group_char_Option_Menu.config(width="3")
        Blood_Group_sign_option_menu = OptionMenu(
            self.scr, self.blood_grp_sign, "+", "-").grid(row=6, column=2)

        # --> Mobile Label And Entry
        mob_label = self.tag(self.scr, "Mobile No.", 5, 8, 0)
        mob_entry = self.entry(self.scr, 5, self.mob, 8, 1)
        self.nl(9)

        # --> Get today's Date
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        self.today = str(month) + "/" + str(day) + "/" + str(year)[-2:]

        # --> Date Label && Entry
        date_label = self.tag(self.scr, "DATE (mm/dd/yy)", 5, 10, 0,
                              padx=10, bg="burlywood1", font="Ubuntu 12 bold")
        self.selected_date = Label(
            self.scr, text=self.today, bd=5, bg="burlywood1", padx=5, font="Ubuntu 14")
        self.selected_date.grid(row=10, column=1)

        # --> Choose Date
        date_btn = Button(self.scr, text="Schedule Date", command=self.cal,
                          bd=5, bg="SlateBlue1", foreground="white")
        date_btn.grid(row=10, column=2)
        date_btn.config(font="Ubuntu 12 bold")

        # --> City Label And Entry
        City_label = self.tag(self.scr, "City", 5, 12, 0)
        City_entry = self.entry(self.scr, 5, self.city, 12, 1)

        # --> Some Buttons
        store_btn = self.btn(
            self.scr, "Store", self.validation, 10, 14, 0, bg="silver")
        reset_btn = self.btn(self.scr, "Reset", self.reset,
                             10, 14, 1, columnspan=2, bg="silver")
        cancel_btn = self.btn(
            self.scr, "Back", self.scr.destroy, 10, 14, 3, bg="silver")

        self.scr.mainloop()

    def receiver(self):
        self.scr_2 = Toplevel(self.home)
        self.scr_2.attributes("-topmost", 1)
        self.scr_2.iconbitmap(cwd + r"\Blood.ico")
        self.scr_2.title("Blood Bank System")
        self.scr_2.config(bg="silver")
        self.scr_2.geometry("590x500+400+100")
        self.scr_2.resizable(width=False, height=False)
        self.scr_2.grid_columnconfigure(1, minsize=200)
        self.scr_2.grid_columnconfigure(2, minsize=200)
        self.scr_2.grid_columnconfigure(3, minsize=200)

        # canvas = Canvas(self.scr_2, width=600, height=500)
        # image_1 = ImageTk.PhotoImage(Image.open("C:/Python/Project/img4.jpg"))
        # canvas.create_image(0,0, anchor=NW, image=image_1)
        # canvas.grid(row=0, column=0, rowspan=10, columnspan=10)
        # # Label(self.scr_2,text="duhfuihiudhs").grid(row=0,column=0)

        # with open("blood_bank_status.csv", "r")as bbs:
        #     reader = csv.reader(bbs)
        #     temp = []
        #     for x in reader:
        #         temp.append(x)

        l = demo.bank_data()

        w.tag(self.scr_2, "Blood Group", 5, 0, 0,
              bg="Silver", pady=5, font="Ubuntu 18 bold")
        for x in range(8):
            Label(self.scr_2, text=l[x][0], bd=5, width="5", bg="white", font="Ubuntu 14").grid(
                row=x + 1, column=0)

        for x in range(1, 9):
            w.tag(self.scr_2, "---------->", 5, x, 1, pady=5, bg="silver")

        w.tag(self.scr_2, "Units Available", 5, 0, 2,
              bg="Silver", font="Ubuntu 18 bold")

        for x in range(8):
            w.tag(self.scr_2, l[x][1], 5, x + 1, 2,
                  font="Ubuntu 14", pady=2, padx=80)

        Label(self.scr_2, bg="silver").grid(row=9)
        Button(self.scr_2, text="Request", command=self.blood_request,
               font="Ubuntu 16 bold", bd=5, padx=5).grid(row=10, column=0)
        Button(self.scr_2, text="Back", command=self.scr_2.destroy,
               font="Ubuntu 16 bold", bd=5).grid(row=10, column=2)

        # w.tag(self.scr_2,"WWWWWW",5,0,1)

    def blood_request(self):
        self.scr_2.destroy()

        font1 = "Firefox 14"

        self.req_scr = Toplevel(self.home)
        self.req_scr.iconbitmap(cwd + r"\Blood.ico")
        self.req_scr.title("Blood Bank System")
        self.req_scr.config(bg="silver")
        self.req_scr.geometry("800x520+300+70")
        self.req_scr.resizable(width=False, height=False)
        self.req_scr.grid_rowconfigure(1, minsize=50)
        self.req_scr.grid_rowconfigure(2, minsize=50)
        self.req_scr.grid_rowconfigure(3, minsize=50)
        self.req_scr.grid_rowconfigure(5, minsize=50)
        self.req_scr.grid_rowconfigure(6, minsize=100)
        self.req_scr.grid_rowconfigure(4, minsize=100)

        canvas = Canvas(self.req_scr, width=820, height=530)
        image_1 = ImageTk.PhotoImage(Image.open(cwd + r"\img5.jpg"))
        canvas.create_image(0, 0, anchor=NW, image=image_1)
        canvas.grid(row=0, column=0, columnspan=4, rowspan=20)

        heading = Label(self.req_scr, text="Blood Request Form", font="Ubuntu 18 bold underline", bg="silver", width="56").grid(
            row=0, column=0, columnspan=10, sticky=NW)

        sub_heading = Label(self.req_scr, text="Patient Details:",
                            bd=5, font="Firefox 16 bold", bg="sky blue")
        sub_heading.grid(row=1, column=0)

        # --> Name Label and Entry
        Label(self.req_scr, text="Name", bd=5, width="10",
              font="Firefox 14 bold", bg="white").grid(row=2, column=0)
        self.p_name = StringVar()
        p_name_entry = Entry(
            self.req_scr, textvariable=self.p_name, bd=5, width="15")
        p_name_entry.config(font="Firefox 12")
        p_name_entry.grid(row=2, column=1, ipady=3)

        # --> Age Label & Entry
        Label(self.req_scr, text="Age", bd=5, width="10",
              font="Firefox 14 bold", bg="white").grid(row=2, column=2)
        self.p_age = StringVar()
        p_age_entry = Entry(
            self.req_scr, textvariable=self.p_age, bd=5, width="8")
        p_age_entry.config(font="Ubuntu 13")
        p_age_entry.grid(row=2, column=3, pady=5, ipady=3)

        # --> Blood Group Label And OptionMenu
        self.p_blood_grp = StringVar()
        self.p_blood_grp.set("A+")

        Label(self.req_scr, text="Blood Group", bd=5, width="10",
              font="Firefox 14 bold", bg="white").grid(row=3, column=0)
        p_bg_menu = OptionMenu(self.req_scr, self.p_blood_grp,
                               "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")
        p_bg_menu.grid(row=3, column=1)
        p_bg_menu.config(width="3", font="Ubuntu 13")
        menu = self.req_scr.nametowidget(p_bg_menu.menuname)
        menu.config(font="Firefox 14")

        Label(self.req_scr, text="Prior Diseases", bd=5, width="12",
              font="Firefox 14 bold", bg="white").grid(row=4, column=0, rowspan=2)

        self.chk_btn1 = IntVar()
        self.chk_btn2 = IntVar()
        self.chk_btn3 = IntVar()
        self.chk_btn4 = IntVar()

        Button1 = Checkbutton(self.req_scr, text="Diabetes",
                              variable=self.chk_btn1,
                              onvalue=1,
                              offvalue=0,
                              height=2,
                              width=10)

        Button2 = Checkbutton(self.req_scr, text="High BP",
                              variable=self.chk_btn2,
                              onvalue=1,
                              offvalue=0,
                              height=2,
                              width=10)

        Button3 = Checkbutton(self.req_scr, text="Anemia",
                              variable=self.chk_btn3,
                              onvalue=1,
                              offvalue=0,
                              height=2,
                              width=10)

        Button4 = Checkbutton(self.req_scr, text="Hemophilia",
                              variable=self.chk_btn4,
                              onvalue=1,
                              offvalue=0,
                              height=2,
                              width=10)

        Button1.config(font=font1)
        Button2.config(font=font1)
        Button3.config(font=font1)
        Button4.config(font=font1)

        Button1.grid(row=4, column=1)
        Button2.grid(row=4, column=2)
        Button3.grid(row=5, column=1)
        Button4.grid(row=5, column=2)

        # --> Mobile Number
        Label(self.req_scr, text="Mobile Number", bd=5, width="13",
              font="Firefox 14 bold", bg="white").grid(row=6, column=0)
        self.p_mob = StringVar()
        p_mob_entry = Entry(
            self.req_scr, textvariable=self.p_mob, bd=5, width="15")
        p_mob_entry.config(font="Ubuntu 13")
        p_mob_entry.grid(row=6, column=1, pady=5, ipady=3)

        # ---> Back && Submit Button
        self.btn(self.req_scr, "Back",
                 self.req_scr.destroy, 8, 7, 2, bg="silver")
        self.btn(self.req_scr, "Submit",
                 self.req_form_validation, 8, 7, 1, bg="silver")

        self.req_scr.mainloop()

    def homescr(self):

        self.home = Tk()
        self.home.title("Blood Bank")
        self.home.iconbitmap(cwd + r"\Blood.ico")
        self.home.geometry("550x400+400+150")
        self.home.resizable(width=False, height=False)
        self.home.grid_rowconfigure(4, minsize=100)

        canvas = Canvas(self.home, width=550, height=450)
        image = ImageTk.PhotoImage(Image.open(cwd + r"\img.jpg"))
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.grid(row=0, column=0, rowspan=7, columnspan=2)

        heading = Label(self.home, text="Blood Bank",
                        bg="silver", width="10", font="Ubuntu 24 bold", bd=5, padx=5).grid(row=1, columnspan=2)

        Label(self.home, text="Hey are you a Donor or Receiver..?",
              bd=5, font="Ubuntu 20", padx=5, pady=5, width="27", bg="silver").grid(row=2, columnspan=2)

        self.status = StringVar()
        self.status.set("Donor")
        Options = OptionMenu(self.home, self.status, "Donor", "Receiver")
        Options.grid(row=3, columnspan=2)
        Options.config(font="Ubuntu 20")
        menu = self.home.nametowidget(Options.menuname)
        menu.config(font="Ubuntu 20")

        self.home.grid_rowconfigure(3, minsize=100)
        self.home.grid_rowconfigure(2, minsize=50)

        Button(self.home, text="Click Me", command=self.chk,
               bd=5, font="Ubuntu 20", bg="silver").grid(row=4, column=0)
        Button(self.home, text="Cancel", command=lambda: self.quit(self.home),
               bd=5, font="Ubuntu 20", bg="silver").grid(row=4, column=1)

        self.home.mainloop()


if __name__ == "__main__":
    m = Main()
    m.homescr()
