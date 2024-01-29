import tkinter as tk
from time import sleep, time


class ChatWidget(tk.Frame):
    
    def __init__(self, master=None, Title="Chat Window", **kwargs):
        super().__init__(master, **kwargs)
        self.pack()
        self.create_widgets()
        self.text = ""
        self.winfo_toplevel().title(Title)

    def create_widgets(self):
        '''makes a beutiful widget for the window complete with a text box, entry bar, and scroll bar'''
              
        self.message_box = tk.Text(self, height=10, width=50, borderwidth=2, relief="groove")
        self.message_box.config(state='disabled')
        
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.message_box.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.message_box.config(yscrollcommand=self.scrollbar.set)
        
        self.message_box.pack(side="top", padx=5, pady=5)
        
        self.input_bar = tk.Entry(self, width=50, borderwidth=2, relief="groove")
        self.input_bar.pack(side="bottom", padx=5, pady=5)
        self.input_bar.bind("<Return>", self.send_message)

    def send_message(self,event):
        '''adds the messgae entered into the imput bar and makes it the latest cannonically entred message'''
        message = self.input_bar.get()
        if (not message.isspace()):
            self.input_bar.delete(0, "end")
            self.message_box.config(state='normal')
            self.add_message("you: "+ message )
            self.message_box.config(state='disabled')
            self.text = message
        else:
            sleep(0.1)

    def get_next_message(self,timeout_seconds=None):
        '''waits until a the self.text of the window cannonically changes and returns the new one,
        this should happen when a messege is entered, breaks when the epoch's limit is reached'''
        #start_time = time.time()
        #print("waiting for entry...")
        preText=self.text
        try:
            while (self.check_exists and preText==self.text):
                #if ((not timeout_seconds==None) and ((time.time() - start_time) > timeout_seconds)):
                #    return preText
                sleep(0.1)
            message = self.text
            self.text = ""
            return message
        except: return preText

    def add_message(self, message):
        '''adds the text to the box without it being entered or changing the latest cannonically entered message'''
        if (not message==None):
            try:
                self.message_box.config(state='normal')
                self.message_box.insert("end", message + "\n")
                self.message_box.config(state='disabled')
                self.message_box.see("end")
            except: print ()
        
    def check_exists(self):
        '''check if the window exists'''
        try:
            return self.winfo_exists()
        except tk.TclError:
            return False

class Main:
    def __init__(self):
        self.chat_widget = ChatWidget(Title="Test Window")
        self.chat_widget.pack(padx=10, pady=10)
        self.chat_widget.add_message("Welcome to the chat widget!")
        #self.send_message()


if __name__ == "__main__":
    main = Main()
    main.chat_widget.mainloop()
    while (main.chat_widget.check_exists()):
        sleep(1)

