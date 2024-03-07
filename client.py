import tkinter
from tkinter import *
from  ttkwidgets import *
import mysql.connector
from tkinter import messagebox
from tkinter import scrolledtext
from socket import *
from threading import *
from tkinter import END
import threading
import socket

HOST = '127.0.0.1'
PORT = 5555
    
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


root = tkinter.Tk()
root.geometry("600x650")
root.title("DISCORD")
root.config(bg="black")


connecter = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "MyDiscord"
)
cursor = connecter.cursor()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class page_inscription:
    def __init__(self, master):
        self.master = master
    
    def open_inscription(self):
        inscription_root = Toplevel(self.master)
        inscription_root.geometry("600x650")
        inscription_root.title("inscription")
        inscription_root.config(bg="grey")

        titre1_label = Label(inscription_root, text="Saisissez vos informations", font= "size=25", bg="grey", fg="white")
        titre1_label.place(x=130, y=10)
        titre2_label = Label(inscription_root, text="d'inscription",font= "size=25", bg="grey", fg="white")
        titre2_label.place(x=180, y=40)

        self.nom_inscription = Label(inscription_root, text="Nom", bg="grey", fg="white")
        self.nom_inscription.place(x=100, y=80)
        self.nom_entry = Entry(inscription_root, width=48 )
        self.nom_entry.place(x=100, y=100)

        self.prenom_inscription = Label(inscription_root, text="Prenom", bg="grey", fg="white")
        self.prenom_inscription.place(x=100, y=130)
        self.prenom_entry = Entry(inscription_root, width=48 )
        self.prenom_entry.place(x=100, y=150)

        self.email_inscription = Label(inscription_root, text="Email", bg="grey", fg="white")
        self.email_inscription.place(x=100, y=180)
        self.email_entry = Entry(inscription_root, width=48 )
        self.email_entry.place(x=100, y=200)

        self.password_inscription = Label(inscription_root, text="password", bg="grey", fg="white")
        self.password_inscription.place(x=100, y=230)
        self.password_entry = Entry(inscription_root, width=48 )
        self.password_entry.place(x=100, y=250)

        self.btn_inscription = Button(inscription_root, text="S'inscrire", width=40, bg="blueviolet", fg="white", command=self.inscription_database)
        self.btn_inscription.place(x=100, y=300)
    
    def inscription_database(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        cursor = connecter.cursor()
        sql = "INSERT INTO user (nom, prenom, email, password) VALUES (%s, %s, %s, %s)"
        val = (nom, prenom, email, password)
        cursor.execute(sql, val)
        connecter.commit()
        print(cursor.rowcount, "personne inscrite")

        self.nom_entry.delete(0, END)
        self.prenom_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)


        cursor.close()
        connecter.close()

if connecter.is_connected:
    print("access à la base de donée")
    mon_inscription = page_inscription(root)



        

class connexion_page:
    def __init__(self, master):
        self.master = master
        
    def open_login(self):
        connexion_root = Toplevel(self.master)
        connexion_root.geometry("500x350")
        connexion_root.title("Connexion")
        connexion_root.config(bg="grey")

        self.titre1_label = Label(connexion_root, text="Ha, te revoila !", font= "size=25", bg="grey", fg="white")
        self.titre1_label.pack()
        self.titre2_label = Label(connexion_root, text="Nous sommes siheureux de te revoir !", bg="grey", fg="white")
        self.titre2_label.place(x=160, y=40)


        self.nom_label = Label(connexion_root, text="Nom", bg="grey", fg="white")
        self.nom_label.place(x=100, y=80)
        self.nom_entry = Entry(connexion_root, width=48 )
        self.nom_entry.place(x=100, y=100)
        self.password_label = Label(connexion_root, text="password", bg="grey", fg="white")
        self.password_label.place(x=100, y=130)
        self.password_entry = Entry(connexion_root, width=48, show="*")
        self.password_entry.place(x=100, y=150)
        
        

        self.btn_connexion = Button(connexion_root, text="connexion", width=40, bg="blueviolet", fg="white", command=self.connexion_database)
        self.btn_connexion.place(x=100, y=200)

    def connexion_database(self):
        nom = self.nom_entry.get()
        password = self.password_entry.get()

        cursor = connecter.cursor()
        sql = "SELECT * FROM user WHERE nom=%s AND password=%s"
        val = (nom, password)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result:
            return accueil.open_accueil()
            
        else:
            messagebox.showerror("Erreur", "Nom ou mot de passe incorrect")
        
        self.nom_entry.delete(0, END)
        self.password_entry.delete(0, END)
        cursor.close()

if connecter.is_connected:
    se_connecter = connexion_page(root)   


class page_accueil:
    def __init__(self, master):
        self.master = master 
        self.clientSocket = None


    def add_message(self,message):
        self.message_box.config(state=NORMAL)
        self.message_box.insert(END, message + '\n')
        self.message_box.config(state=DISABLED)

    def connect(self):

        try:

            self.clientSocket.connect((HOST, PORT))
            print("Successfully connected to server")
            self.add_message("[SERVER] Successfully connected to the server")
        except:
            messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

        username = self.username_textbox.get()
        if username != '':
            client.sendall(username.encode())
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")

        threading.Thread(target=self.listen_for_messages_from_server, args=(self.clientSocket, )).start()

        self.username_textbox.config(state=DISABLED)
        self.username_button.config(state=DISABLED)


    def send_message(self):
        message = self.message_textbox.get()
        if message != '':
            client.sendall(message.encode())
            self.message_textbox.delete(0, len(message))
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def open_accueil(self):
        
        

        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=4)
        root.grid_rowconfigure(2, weight=1)

        top_frame = Frame(root, width=600, height=100, bg=DARK_GREY)
        top_frame.grid(row=0, column=0, sticky=NSEW)

        middle_frame = Frame(root, width=600, height=400, bg=MEDIUM_GREY)
        middle_frame.grid(row=1, column=0, sticky=NSEW)

        bottom_frame = Frame(root, width=600, height=100, bg=DARK_GREY)
        bottom_frame.grid(row=2, column=0, sticky=NSEW)

        username_label = Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
        username_label.pack(side=LEFT, padx=10)

        username_textbox = Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
        username_textbox.pack(side=LEFT)

        self.username_button = Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.connect)
        self.username_button.pack(side=LEFT, padx=15)

        message_textbox = Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
        message_textbox.pack(side=LEFT, padx=10)

        self.message_button = Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.send_message)
        self.message_button.pack(side=LEFT, padx=10)

        message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
        message_box.config(state=DISABLED)
        message_box.pack(side=TOP)

    def listen_for_messages_from_server(self, client):

        while 1:

            message = client.recv(5555).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]

                self.add_message(f"[{username}] {content}")
            
            else:
                messagebox.showerror("Error", "Message recevied from client is empty")    
    
accueil = page_accueil(root)

label = tkinter.Label(root, text="myDiscord", fg="white", bg="black", font= "size=25")
label.place(x=250, y=50)

label = tkinter.Label(root, text="Bienvenue  sur  My Discord", fg="white", bg="black", font= "size=19")
label.place(x=200, y=330)
inscription = tkinter.Button(root, text="S'inscrire", width=50, bg="blueviolet", fg="white", highlightthickness=0, command=mon_inscription.open_inscription)
inscription.place(x=105, y=500)
inscription.configure(bd=0)
connexion = tkinter.Button(root, text="connexion", width=50, bg="blueviolet", fg="white", highlightthickness=0, command=se_connecter.open_login)
connexion.place(x=105, y=550)
connexion.configure(bd=0)

root.mainloop()
