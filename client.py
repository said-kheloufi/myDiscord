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

# Define server address and port
HOST = '127.0.0.1'
PORT = 5555

# Define color and font constants
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Create the root window
root = tkinter.Tk()
root.geometry("600x650")
root.title("DISCORD")
root.config(bg="black")

# Connect to the MySQL database
connecter = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "MyDiscord"
)
cursor = connecter.cursor()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the registration page class
class page_inscription:
    def __init__(self, master):
        self.master = master

    # Function to open the registration page
    def open_inscription(self):
        # Create a new window for the registration page
        inscription_root = Toplevel(self.master)
        inscription_root.geometry("600x650")
        inscription_root.title("inscription")
        inscription_root.config(bg="grey")

        # Create labels and entry fields for the registration form
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

        # Create a button to submit the registration form
        self.btn_inscription = Button(inscription_root, text="S'inscrire", width=40, bg="blueviolet", fg="white", command=self.inscription_database)
        self.btn_inscription.place(x=100, y=300)

    # Function to insert the registration data into the database
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

        # Clear the entry fields after submitting the form
        self.nom_entry.delete(0, END)
        self.prenom_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)

        cursor.close()
        connecter.close()

# Check if the database connection is successful
if connecter.is_connected:
    print("access à la base de donée")
    mon_inscription = page_inscription(root)

# Define the login page class
class connexion_page:
    def __init__(self, master):
        self.master = master

    # Function to open the login page
    def open_login(self):
        # Create a new window for the login page
        connexion_root = Toplevel(self.master)
        connexion_root.geometry("500x350")
        connexion_root.title("Connexion")
        connexion_root.config(bg="grey")

        # Create labels and entry fields for the login form
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

        # Create a button to submit the login form
        self.btn_connexion = Button(connexion_root, text="connexion", width=40, bg="blueviolet", fg="white", command=self.connexion_database)
        self.btn_connexion.place(x=100, y=200)

    # Function to check the login data in the database
    def connexion_database(self):
        nom = self.nom_entry.get()
        password = self.password_entry.get()

        cursor = connecter.cursor()
        sql = "SELECT * FROM user WHERE nom=%s AND password=%s"
        val = (nom, password)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        # If the login data is correct, open the home page
        if result:
            return accueil.open_accueil()

        # If the login data is incorrect, show an error message
        else:
            messagebox.showerror("Erreur", "Nom ou mot de passe incorrect")

        # Clear the entry fields after submitting the form
        self.nom_entry.delete(0, END)
        self.password_entry.delete(0, END)
        cursor.close()

# Check if the database connection is successful
if connecter.is_connected:
    se_connecter = connexion_page(root)

# Define the home page class
class page_accueil:
    def __init__(self, master):
        self.master = master
        self.clientSocket = None

    # Function to add a message to the chat box
    def add_message(self,message):
        self.message_box.config(state=NORMAL)
        self.message_box.insert(END, message + '\n')
        self.message_box.config(state=DISABLED)

    # Function to connect to the chat server
    def connect(self):
        try:
            # Try to connect to the server
            self.clientSocket.connect((HOST, PORT))
            print("Successfully connected to server")
            self.add_message("[SERVER] Successfully connected to the server")
        except:
            # If the connection fails, show an error message
            messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

        # Get the username from the entry field
        username = self.username_textbox.get()
        if username != '':
            # If the username is not empty, send it to the server
            client.sendall(username.encode())
        else:
            # If the username is empty, show an error message
            messagebox.showerror("Invalid username", "Username cannot be empty")

        # Start a new thread to listen for messages from the server
        threading.Thread(target=self.listen_for_messages_from_server, args=(self.clientSocket, )).start()

        # Disable the username entry field and button after connecting to the server
        self.username_textbox.config(state=DISABLED)
        self.username_button.config(state=DISABLED)

    # Function to send a message to the server
    def send_message(self):
        # Get the message from the entry field
        message = self.message_textbox.get()
        if message != '':
            # If the message is not empty, send it to the server
            client.sendall(message.encode())
            # Clear the entry field after sending the message
            self.message_textbox.delete(0, len(message))
        else:
            # If the message is empty, show an error message
            messagebox.showerror("Empty message", "Message cannot be empty")

    # Function to open the home page
    def open_accueil(self):
        # Configure the grid layout for the root window
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=4)
        root.grid_rowconfigure(2, weight=1)

        # Create frames for the top, middle, and bottom sections of the window
        top_frame = Frame(root, width=600, height=100, bg=DARK_GREY)
        top_frame.grid(row=0, column=0, sticky=NSEW)

        middle_frame = Frame(root, width=600, height=400, bg=MEDIUM_GREY)
        middle_frame.grid(row=1, column=0, sticky=NSEW)

        bottom_frame = Frame(root, width=600, height=100, bg=DARK_GREY)
        bottom_frame.grid(row=2, column=0, sticky=NSEW)

        # Create labels, entry fields, and buttons for the chat interface
        username_label = Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
        username_label.pack(side=LEFT, padx=10)

        self.username_textbox = Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
        self.username_textbox.pack(side=LEFT)

        self.username_button = Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.connect)
        self.username_button.pack(side=LEFT, padx=15)

        self.message_textbox = Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
        self.message_textbox.pack(side=LEFT, padx=10)

        self.message_button = Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.send_message)
        self.message_button.pack(side=LEFT, padx=10)

        self.message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
        self.message_box.config(state=DISABLED)
        self.message_box.pack(side=TOP)

    # Function to listen for messages from the server
    def listen_for_messages_from_server(self, client):
        while 1:
            # Receive a message from the server
            message = client.recv(5555).decode('utf-8')
            if message != '':
                # If the message is not empty, split it into the username and content
                username = message.split("~")[0]
                content = message.split('~')[1]

                # Add the message to the chat box
                self.add_message(f"[{username}] {content}")
            else:
                # If the message is empty, show an error message
                messagebox.showerror("Error", "Message received from client is empty")

# Create an instance of the home page class
accueil = page_accueil(root)

# Create labels and buttons for the main page
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

# Start the main event loop
root.mainloop()
