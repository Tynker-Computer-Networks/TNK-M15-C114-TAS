import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None
font_size = None
image=None

SERVER = None
PORT = None
IP_ADDRESS = None
canvas1 = None

player_name = None
name_entry = None
name_window = None

# Create variable left_boxes
left_boxes = []

# Define left_board() function
def left_board():
    # Access game_window, left_boxes, screen_height, screen_width as global
    global game_window, left_boxes, screen_height, screen_width 
    
    # Set box_width to 50th of screen_width
    box_width = int(screen_width/50)

    # set xPos to box_width i.e starting point of the boxes
    xPos = box_width
    # Create a for loop to run for box in range 0,10 
    for box in range(0,10):
        # check if box is 0 i.e starting box
        if(box == 0):
            # Create a label box_label, set font width using box_width, width to 2, height to 1, borderwidth to 0 and bg to red
            box_label = Label(game_window, font=("Helvetica",box_width), width=2, height=1, borderwidth=0, bg="red")
        # Else
        else:
            # Create a label named box_label of color white
            box_label = Label(game_window, font=("Helvetica",box_width), width=2, height=1, borderwidth=0, bg="white")
        
        # Set x and y pos of box_label to xPos and screen_height/3 
        box_label.place(x=xPos, y=screen_height/3)
        # Add box_label to left_boxes
        left_boxes.append(box_label)
        # Increment the xPos by box_width*2
        xPos += box_width*2

# Explain game() function
def game():
    global game_window, canvas2, screen_width, screen_height, dice, wining_message, font_size, image

    game_window = Tk()
    game_window.title("Ludo Ladder")

    bg = ImageTk.PhotoImage(image)
    
    canvas2 = Canvas( game_window, width = screen_width, height = screen_height)
    canvas2.pack(fill = "both", expand = True)
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")
    canvas2.create_text( screen_width/2, screen_height/8, text = "Ludo Ladder", font=("Chalkboard SE", font_size), fill="white")

    # Call method left_board(0 to create left board on the screen)
    left_board()
    
    game_window.resizable(True, True)
    game_window.mainloop()

def save_name():
    global SERVER, player_name, name_window, name_entry
    player_name = name_entry.get()
    name_entry.delete(0, END)
    name_window.destroy()

    SERVER.send(player_name.encode())
     
    # Call game function to open the game 
    game()


def ask_player_name():
    global player_name, name_entry, name_window, canvas1, font_size, screen_width, screen_height, image
    name_window  = Tk()
    name_window.title("Ludo Ladder")

    screen_width = name_window.winfo_screenwidth()
    screen_height = name_window.winfo_screenheight()

    font_size = int(screen_width * 0.03)

    image = Image.open("./assets/background.png")
    image = image.resize((screen_width, screen_height))
    bg = ImageTk.PhotoImage(image)
    
    canvas1 = Canvas( name_window, width = screen_width,height = screen_width)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",font_size), fill="white")

    name_entry = Entry(name_window,  justify='center', font=('Chalkboard SE', font_size), bd=5, bg='white')
    name_entry.place(relx = 0.25, rely=0.3, relwidth = 0.5)
    
    button = Button(name_window, text="Save", font=("Chalkboard SE", font_size), command=save_name, height=1, bg="#80deea", bd=3)
    button.place(relx= 0.33, rely=0.5, relwidth = 0.34)

    name_window.resizable(True, True)
    name_window.mainloop()

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    ask_player_name()

setup()
