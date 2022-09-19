import datetime
import json
import textwrap
import time
import tkinter.messagebox
from tkinter import *
from tkinter import font
from tkinter.ttk import Treeview
from tkcalendar import Calendar
import smtplib



class Main(Frame):
    def __init__(self, root):
        super().__init__()
        self.photo = PhotoImage(file='main_pic.png')
        self.init_main()

    def init_main(self):
        canvas = Canvas(frame, height=400, width=600, bg='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=self.photo)

        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(family="Segoe Script", size=25, weight=font.BOLD)

        Label(frame, text="CALENDAR", fg="purple", bg='white',
              height=0, width=10).place(x=200, y=50)
        Label(frame, text="Login:", fg="purple", bg='white', font="Arial 15",
              height=1, width=10).place(x=140, y=135)
        Label(frame, text="Password:", fg="purple", bg='white', font="Arial 15",
              height=1, width=10).place(x=140, y=185)
        Label(frame, text="You can login in your Yandex mail!", fg="gray", bg='white',font="Arial 13",
              height=0, width=30).place(x=180, y=220)

        self.entry_login = Entry(frame, bg='white', font="Arial 15", width=17)
        self.entry_login.place(x=263, y=137)
        self.entry_password = Entry(frame, bg='white', font="Arial 15", show='*', width=17)
        self.entry_password.place(x=263, y=185)

        button_reg = Button(frame, text="Start", fg="purple", bg='white', height=1, width=15,
                            font="Arial 15")
        button_reg.config(command=self.start_child)
        button_reg.place(x=230, y=250)

    def start_child(self):
        self.login, self.password = self.reg()
        for widget in frame.winfo_children():
            widget.destroy()
        Child(tk)

    def reg(self):
        return self.entry_login.get(), self.entry_password.get()


class Child(Frame):
    def __init__(self, root):
        super().__init__()
        self.add_img = PhotoImage(file="add_pic.png")
        self.delete_img = PhotoImage(file="delete_pic.png")
        self.sent_img = PhotoImage(file="sent_pic.png")
        self.back_img = PhotoImage(file="back_pic.png")
        self.init_child()

    def init_child(self):
        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(family='Arial', size=10, weight=font.BOLD)

        now = datetime.datetime.now()
        self.label_time = Label(frame, font=("Arial", 29, "bold"), bg="white", text=time.strftime("%H:%M:%S"),
                                fg='purple',
                                height=0, width=10)
        self.label_time.place(x=375, y=0)
        self.update_time()

        self.calendar = Calendar(frame, font="Arial 16", selectmode='day', year=now.year, month=now.month, day=now.day,
                                 borderwidth=0, background="purple", foreground="white",
                                 headersbackground="white", headersforeground="purple",
                                 selectbackground="purple", weekendbackground='white')
        self.calendar.place(x=0, y=35)

        btn_delete = Button(frame, text="Delete event", fg="purple", bg='white', height=100, width=110,
                            font="Arial 15", compound=TOP, image=self.delete_img, bd=0)
        btn_delete.config(command=self.delete_vent)
        btn_delete.place(x=20, y=290)

        btn_add = Button(frame, text="Add event", fg="purple", bg='white', height=100, width=100,
                         font="Arial 15", compound=TOP, image=self.add_img, bd=0)
        btn_add.config(command=Add)
        btn_add.place(x=170, y=290)

        btn_sent = Button(frame, text="Send", fg="purple", bg='white', height=100, width=100,
                          font="Arial 15", compound=TOP, image=self.sent_img, bd=0)
        btn_sent.config(command=Message)
        btn_sent.place(x=300, y=290)

        btn_back = Button(frame, text="Back", fg="purple", bg='white', height=100, width=100,
                          font="Arial 15", compound=TOP, image=self.back_img, bd=0)
        btn_back.config(command=self.back_child)
        btn_back.place(x=430, y=290)

        frame_tree = Frame(frame, height=100, width=110)
        frame_tree.place(x=400, y=45)

        self.tree = Treeview(frame_tree, columns=('Date', 'Event'), height=11, show='headings')
        self.tree.column('Date', width=55, anchor=CENTER)
        self.tree.column('Event', width=110, anchor=CENTER)
        self.tree.heading('Date', text='Date')
        self.tree.heading('Event', text='Event')
        self.tree.pack(side=LEFT)

        scroll = Scrollbar(frame_tree, command=self.tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scroll.set)

        self.view_record(self)

        self.calendar.bind("<<CalendarSelected>>", self.view_record)

    def view_record(self, event):
        with open("data.json", "r", encoding="UTF-8") as read_file:
            date = json.load(read_file)
        with open("your_data.json", "r", encoding="UTF-8") as read_file:
            your_date = json.load(read_file)
        [self.tree.delete(i) for i in self.tree.get_children()]
        if self.calendar.get_date() in date:
            [self.tree.insert('', 0, values=(self.calendar.get_date(), self.wrap(row)))
             for row in date[self.calendar.get_date()]]
        if self.calendar.get_date() in your_date:
            [self.tree.insert('', END, values=(self.calendar.get_date(), self.wrap(row)))
             for row in your_date[self.calendar.get_date()]]

    def update_time(self):
        if self.label_time is not None:
            self.label_time.config(text=time.strftime("%H:%M:%S"))
            tk.after(200, self.update_time)

    def delete_vent(self):
        with open("data.json", "r", encoding="UTF-8") as read_file:
            date = json.load(read_file)
        with open("your_data.json", "r", encoding="UTF-8") as read_file:
            your_date = json.load(read_file)
        try:
            values = self.tree.item(self.tree.selection(), option='values')
            if date.get(values[0]):
                if values[1].replace('\n', '') in date[values[0]]:
                    date[values[0]].remove(values[1].replace('\n', ''))
            if your_date.get(values[0]):
                if values[1].replace('\n', '') in your_date[values[0]]:
                    your_date[values[0]].remove(values[1].replace('\n', ''))
        except:
            tkinter.messagebox.showwarning(title="Warning", message="Choose event for deleting!")

        with open("data.json", "w") as write_file:
            json.dump(date, write_file)
        with open("your_data.json", "w") as write_file:
            json.dump(your_date, write_file)

        self.view_record(self)

    def back_child(self):
        self.label_time = None
        Main(tk)

    def wrap(self, string, lenght=20):
        return '\n'.join(textwrap.wrap(string, lenght))


class Add(Toplevel):
    def __init__(self):
        super().__init__()
        self.init_add()

    def init_add(self):
        frame_date = Frame(self, bg='white', height=300, width=500)
        frame_date.pack()

        Label(frame_date, text="Enter date:", fg="purple", bg='white', font="Arial 15",
              height=1, width=10).place(x=75, y=50)
        Label(frame_date, text="Event name:", fg="purple", bg='white', font="Arial 15",
              height=1, width=10).place(x=70, y=130)
        Label(frame_date, text="Example: 9/9/22, 12/24/22", fg="gray", bg='white', font="Arial 10",
              height=1, width=25).place(x=180, y=80)

        self.entry_date = Entry(frame_date, bg='white', font="Arial 15", width=17)
        self.entry_date.place(x=190, y=50)
        self.entry_event = Entry(frame_date, bg='white', font="Arial 15", width=17)
        self.entry_event.place(x=190, y=130)

        btn_add = Button(frame_date, text="Add event", fg="purple", bg='white', height=1, width=12,
                         font="Arial 15")
        btn_add.config(command=self.add_event)
        btn_add.place(x=180, y=200)

    def add_event(self):
        with open("your_data.json", "r", encoding="UTF-8") as read_file:
            date = json.load(read_file)
            date.setdefault(self.entry_date.get(), []).append(self.entry_event.get())

        with open("your_data.json", "w") as write_file:
            json.dump(date, write_file)


class Message(Toplevel):
    def __init__(self):
        super().__init__()
        self.init_msg()

    def init_msg(self):
        self.frame_msg = Frame(self, bg='white', height=300, width=500)
        self.frame_msg.pack()

        self.entry_address = Entry(self.frame_msg, bg='white', font="Arial 15", width=30)
        self.entry_address.place(x=140, y=30)

        Label(self.frame_msg, text="Enter yandex:", fg="purple", bg='white', font="Arial 15",
              height=1, width=10).place(x=20, y=30)

        self.text = Text(self.frame_msg, bg='white', font="Arial 15", width=40, height=8)
        self.text.place(x=30, y=60)

        self.btn_sent = Button(self.frame_msg, text="Sent message", fg="purple", bg='white', height=1, width=15,
                               font="Arial 15")
        self.btn_sent.config(command=self.connect)
        self.btn_sent.place(x=300, y=250)

    def connect(self):
        try:
            letter = f"""\
            From: {app.login}
            To: {self.entry_address.get()}
            Subject: Поздравление!
            Content-Type: text/plain; charset="UTF-8";
            
            {self.text.get("1.0", END)}"""
            letter = letter.encode("UTF-8")
            server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
            server.login(app.login, app.password)
            server.sendmail(app.login, self.entry_address.get(), letter)
            server.quit()

            Label(self.frame_msg, text="Message sent!:)", fg="green", bg='white', font="Arial 15",
                  height=1, width=15).place(x=90, y=260)

        except smtplib.SMTPResponseException as e:
            Label(self.frame_msg, text="Bad. Check all!:(", fg="red", bg='white', font="Arial 15",
                  height=1, width=24).place(x=15, y=260)
        except:
            Label(self.frame_msg, text="No connection:(", fg="red", bg='white', font="Arial 15",
                  height=1, width=24).place(x=15, y=260)


if __name__ == "__main__":
    tk = Tk()
    frame = Frame(tk, bg="white")
    frame.pack()
    app = Main(tk)
    tk.title("Event")
    tk.geometry("600x400")
    tk.resizable(False, False)
    tk.mainloop()
