# IMPORTS
from tkinter import messagebox
import tkinter as tk
import json
from datetime import datetime
import random
import textwrap

# VARIABLES
date = datetime.today().strftime('%Y-%m-%d')
chosen_lang = []
greeting = []   
farewell = []


# LANGUAGE RANDOMIZATION
with open('', 'r') as file:
    data = json.load(file)

lang = random.choice(data)
chosen_lang.append(lang)
greeting.append(lang['greeting']) 
farewell.append(lang['farewell'])  

# LOCAL METHODS
def login(username, password):
    if username == '' and password == '':
        frame.destroy()
        root.title('qtMindset')
        inside(username)
    elif username == '' or password == '':
        messagebox.showerror("Error", "All fields required")
    else:
        messagebox.showerror("Error", "Username/password doesn't match the key")

def inside(username):
    # RESPONSIBILITY
    root.geometry("750x400")

    frame_1 = tk.Frame(bg='#333333')
    frame_1.pack()

    # INSIDE WIDGETS
    welcome_label = tk.Label(
        frame_1, 
        text=f'{greeting[0].capitalize()} {username}', 
        bg="#F5B027", 
        fg="#ffffff", 
        font=("Comic Sans", 41)
    )
    empty_label = tk.Label(frame_1, text='', bg='#333333')
    ideas_label = tk.Label(frame_1, text='Your previous ideas', bg='#333333', fg='#ffffff', font=("Comic Sans", 21))
    ideas_button = tk.Button(frame_1, text='Show', bg='#333333', fg='#ffffff', command=lambda: show_ideas(frame_1, username))
    new_idea_label = tk.Label(frame_1, text='Write down below a new idea', bg='#333333', fg='#ffffff', font=('Comic Sans', 21))
    insert_idea = tk.Text(frame_1, height=7, width=35)  
    submit_button = tk.Button(frame_1, text="Submit", bg='#333333', fg='#ffffff', command=lambda: new_idea(insert_idea.get('1.0', 'end-1c')))

    # INSIDE WIDGETS PLACEMENT
    welcome_label.grid(row=0, column=0, columnspan=2, sticky="news")
    empty_label.grid(row=1, column=0)
    ideas_label.grid(row=3, column=0)
    ideas_button.grid(row=3, column=1)
    new_idea_label.grid(row=4, column=0, columnspan=2)
    insert_idea.grid(row=5, column=0)
    submit_button.grid(row=5, column=1)    

def new_idea(idea):
    if idea.strip() == '':
        messagebox.showerror('Error', "U can't save an empty idea")
    else:
        wrapped_idea = textwrap.fill(idea, width=35)
        
        current_date = datetime.today().strftime('%Y-%m-%d')
        
        idea_entry = {
            "date": current_date,
            "idea": wrapped_idea
        }

        try:
            with open('data.json', 'r') as file:
                data = json.load(file) 
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(idea_entry)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success", "You have successfully saved an idea")

def show_ideas(frame_name, username):
    frame_name.destroy()

    frame_2 = tk.Frame(bg='#333333')
    frame_2.pack(fill='both', expand=True)

    top_bar = tk.Frame(frame_2, bg='#333333')
    top_bar.pack(fill='x', pady=10, padx=10)

    back_button = tk.Button(
        top_bar, text='← Back',
        bg='#F5B027', fg='white',
        font=('Comic Sans', 12),
        command=lambda: go_back(frame_2, username)
    )
    back_button.pack(side='left')

    ideas_label = tk.Label(
        top_bar,
        text='Your Saved Ideas',
        bg="#333333", fg="#F5B027",
        font=("Comic Sans", 32)
    )
    ideas_label.pack(side='left', padx=20)

    canvas = tk.Canvas(frame_2, bg='#333333', highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_2, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#333333')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)

        if not data:
            empty_label = tk.Label(
                scrollable_frame,
                text="No ideas yet. Go write some!",
                bg="#333333", fg="white",
                font=("Comic Sans", 18)
            )
            empty_label.pack(pady=20)
            return

        for idx, idea in enumerate(reversed(data), 1):  
            idea_frame = tk.Frame(
                scrollable_frame,
                bg='#F5B027',
                pady=10,
                padx=10,
                bd=2,
                relief='ridge'
            )
            idea_frame.pack(fill='x', pady=10, padx=20)

            date_label = tk.Label(
                idea_frame,
                text=f"{idea['date']}",
                bg='#F5B027', fg='white',
                font=("Comic Sans", 12, "bold"),
                anchor='w'
            )
            date_label.pack(anchor='w')

            idea_text = tk.Label(
                idea_frame,
                text=idea['idea'],
                bg='#F5B027', fg='white',
                font=("Comic Sans", 14),
                wraplength=650,
                justify='left',
                anchor='w'
            )
            idea_text.pack(anchor='w')
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror('Error', "You haven't made any ideas yet.")

def go_back(frame_name, username):
    frame_name.destroy()
    inside(username)
        
    
# MAIN WINDOW
root = tk.Tk()
root.title("Login Page")
root.geometry("500x320")
root.resizable(False, False)
root.configure(bg='#333333')

# RESPONSIBILITY
frame = tk.Frame(bg="#333333")

# LOGIN WIDGETS
login_label = tk.Label(frame, text="qtMindset", bg="#F5B027", fg="#ffffff", font=("Comic Sans", 41)) 
username_entry = tk.Entry(frame)
password_label = tk.Label(frame, text="Password", bg="#333333", fg="#ffffff", font=("Comic Sans", 21))
username_label = tk.Label(frame, text="Username", bg="#333333", fg="#ffffff", font=("Comic Sans", 21))
password_entry = tk.Entry(frame, show="*")
login_button = tk.Button(frame, text="Login", bg="#333333", fg="#ffffff", command=lambda: login(username_entry.get(), password_entry.get()))

# LOGIN WIDGETS PLACEMENT
login_label.grid(row=0, column=0, columnspan=2, sticky="news")
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan=2)

frame.pack()

# MAINLOOP
root.mainloop()
