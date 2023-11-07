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

left_boxes = []
right_boxes = []
finishing_box = None
roll_button =None

# Create player_turn and player_type as global
player_turn = None
player_type = None

def left_board():
    global game_window, left_boxes, screen_height, screen_width 
    
    box_width = int(screen_width/50)
    xPos = box_width

    for box in range(0,10):
        if(box == 0):
            box_label = Label(game_window, font=("Helvetica",box_width), width=2, height=1, borderwidth=0, bg="red")
        else:
            box_label = Label(game_window, font=("Helvetica",box_width), width=2, height=1, borderwidth=0, bg="white")
        
        box_label.place(x=xPos, y=screen_height/3)
        left_boxes.append(box_label)
        xPos += box_width*2

def right_board():
    global game_window, right_boxes, screen_height, screen_width 
    box_width = int(screen_width/50)
    xPos = int(screen_width - box_width*2.5)
    for box in range(0,10):
        if(box == 0):
            box_label = Label(game_window, font=("Helvetica",box_width), width=2, height=1, borderwidth=0, bg="yellow")
        else:
            box_label = Label(game_window, font=("Helvetica",box_width), width=2, height=1, borderwidth=0, bg="white")
        
        box_label.place(x=xPos, y=screen_height/3)
        right_boxes.append(box_label)
        xPos -= box_width*2

def finishing_board():
    global game_window, finishing_box, screen_width, screen_height
    box_width = int(screen_width/50)
    
    finishing_box = Label(game_window, text="Home", font=("Chalkboard SE", box_width), width=10, height=4, borderwidth=0, bg="green", fg="white")
    finishing_box.place(x=screen_width/2 - box_width*4, y=screen_height/3 - box_width*2)

def roll_dice():
    global player_turn, player_type, roll_button
    dice_choices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    value = random.choice(dice_choices)

    # Set player_turn to false
    player_turn = False
    # Destroy roll_button
    roll_button.destroy()

     # if player_type is player1 then send SERVER.send(f'{value}player2_turn'.encode()) otherwise send
    #  SERVER.send(f'{value}player1_turn'.encode()) 
    if(player_type == 'player1'):
        SERVER.send(f'{value}player2_turn'.encode())

    if(player_type == 'player2'):
        SERVER.send(f'{value}player1_turn'.encode())

def received_msg():
    # Access player_type and player_turn, roll_button as global
    global SERVER, canvas2, dice, player_turn, player_type, roll_button
       
    while True:
        message = SERVER.recv(2048).decode()

        if('\u2680' in message):
            canvas2.itemconfigure(dice, text='\u2680')
        elif('\u2681' in message):
            canvas2.itemconfigure(dice, text='\u2681')
        elif('\u2682' in message):
            canvas2.itemconfigure(dice, text='\u2682')  
        elif('\u2683' in message):
            canvas2.itemconfigure(dice, text='\u2683')
        elif('\u2684' in message):
            canvas2.itemconfigure(dice, text='\u2684')
        elif('\u2685' in message):
            canvas2.itemconfigure(dice, text='\u2685')
        # Check if player_type exits in message 
        elif('player_type' in message):
            # Call eval() function with message and store the result in recv_msg
            recv_msg = eval(message)
            # Get player_type from recv_msg
            player_type = recv_msg['player_type']
            # Get player_turn from recv_msg
            player_turn = recv_msg['turn']

        # Check if 'player1_turn' in message and player_type' is player1' or 
        # 'player2_turn' in message and player_type' is player2'
        if(('player1_turn' in message and player_type == 'player1') or
           ('player2_turn' in message and player_type == 'player2')
            ):
            # Set player_turn to True
            player_turn = True
            # Create and place roll_button
            roll_button = Button(game_window,text="Roll Dice", fg='black', font=("Chalkboard SE", int(font_size * 0.5)), bg="grey",command=roll_dice, width=10, height=1)
            roll_button.place(x=(screen_width * 0.5) - font_size*2, y= screen_height * 0.7)

def game():
    global game_window, canvas2, screen_width, screen_height, dice, wining_message, font_size, image, roll_button
    # Access player_type, player_turn as global
    global player_type, player_turn

    game_window = Tk()
    game_window.title("Ludo Ladder")

    bg = ImageTk.PhotoImage(image)
    
    canvas2 = Canvas( game_window, width = screen_width, height = screen_height)
    canvas2.pack(fill = "both", expand = True)
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")
    canvas2.create_text( screen_width/2, screen_height/8, text = "Ludo Ladder", font=("Chalkboard SE", font_size), fill="white")

    left_board()
    right_board()
    finishing_board()
    
    dice = canvas2.create_text(screen_width * 0.5, screen_height * 0.6, text = "\u2680", font=("Chalkboard SE",font_size * 2), fill="white")
    
    roll_button = Button(game_window,text="Roll Dice", fg='black', font=("Chalkboard SE", int(font_size * 0.5)), bg="grey",command=roll_dice, width=10, height=1)
    
    # Place roll_button if player_type is player 1 and player_turn
    if(player_type == 'player1' and player_turn):
        roll_button.place(x=(screen_width * 0.5) - font_size*2, y= screen_height * 0.7)
    # Else call pack_forget() method from roll_button
    else:
        roll_button.pack_forget()

    game_window.resizable(True, True)
    game_window.mainloop()

def save_name():
    global SERVER, player_name, name_window, name_entry
    player_name = name_entry.get()
    name_entry.delete(0, END)
    name_window.destroy()

    SERVER.send(player_name.encode())
     
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

    thread = Thread(target=received_msg)
    thread.start()

    ask_player_name()

setup()
