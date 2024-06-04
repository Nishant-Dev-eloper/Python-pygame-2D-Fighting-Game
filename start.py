import tkinter as tk
from tkinter import messagebox
import subprocess
import pygame
from PIL import Image, ImageTk

def run_game(difficulty):
    pygame.mixer.music.stop()
    if difficulty == "two_players":
        process = subprocess.Popen(["python", "main.py", "two_players"])
    else:
        process = subprocess.Popen(["python", "main.py", difficulty])
    process.wait()  # Wait for the process to finish
    root.deiconify()  # Bring back the game interface window

def exit_game():
    answer = messagebox.askquestion("Exit", "Do you really want to exit the game?")
    if answer == "yes":
        pygame.mixer.music.play()
        root.destroy()

def on_hover(event, button):
    button.config(bg="gray")

def on_leave(event, button):
    button.config(bg="green")   

def choose_difficulty():
    root.withdraw()  # Hide the game interface window
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("Choose Difficulty")
    difficulty_window.geometry("2000x2000")
    difficulty_window.configure(bg='gray')  # Change background color to gray

    try:
        # Load and set the background image using Pillow for JPG support
        bg_image_difficulty = Image.open("second_bg.png")  # Replace with your actual file name
        bg_image_difficulty = ImageTk.PhotoImage(bg_image_difficulty)
        bg_label_difficulty = tk.Label(difficulty_window, image=bg_image_difficulty)
        bg_label_difficulty.image = bg_image_difficulty  # Keep a reference to the image
        bg_label_difficulty.place(relwidth=1, relheight=1)
    except Exception as e:
        print("Error loading second background image:", str(e))

    pygame.mixer.music.load("music.mp3")
    
    # Set the volume to 1.0 for maximum volume
    pygame.mixer.music.set_volume(1.0)
    
    pygame.mixer.music.play(-1)

    difficulty_label = tk.Label(difficulty_window, text="Choose Difficulty Level", font=("Arial", 14), bg='gray', fg='white')  # Change background color to gray
    difficulty_label.pack(pady=(20, 10), side="top", anchor="center")

    button_font = ("Arial", 12)

    def back_to_game_interface():
        difficulty_window.destroy()
        root.deiconify()  # Restore the game interface window

    def run_game_with_difficulty(difficulty):
        run_game(difficulty)
        back_to_game_interface()

    easy_button = tk.Button(difficulty_window, text="Easy", command=lambda: run_game_with_difficulty("easy"), font=button_font, height=2, width=15, bg="green")
    easy_button.pack(pady=(20, 10), side="top", anchor="center")
    easy_button.bind("<Enter>", lambda event: on_hover(event, easy_button))
    easy_button.bind("<Leave>", lambda event: on_leave(event, easy_button))

    medium_button = tk.Button(difficulty_window, text="Medium", command=lambda: run_game_with_difficulty("medium"), font=button_font, height=2, width=15, bg="green")
    medium_button.pack(pady=10, side="top", anchor="center")
    medium_button.bind("<Enter>", lambda event: on_hover(event, medium_button))
    medium_button.bind("<Leave>", lambda event: on_leave(event, medium_button))

    hard_button = tk.Button(difficulty_window, text="Hard", command=lambda: run_game_with_difficulty("hard"), font=button_font, height=2, width=15, bg="green")
    hard_button.pack(pady=10, side="top", anchor="center")
    hard_button.bind("<Enter>", lambda event: on_hover(event, hard_button))
    hard_button.bind("<Leave>", lambda event: on_leave(event, hard_button))

    two_players_button = tk.Button(difficulty_window, text="Two Players", command=lambda: run_game_with_difficulty("two_players"), font=button_font, height=2, width=15, bg="blue")
    two_players_button.pack(pady=10, side="top", anchor="center")
    two_players_button.bind("<Enter>", lambda event: on_hover(event, two_players_button))
    two_players_button.bind("<Leave>", lambda event: on_leave(event, two_players_button))

    back_button = tk.Button(difficulty_window, text="Back", command=back_to_game_interface, font=button_font, height=2, width=15, bg="red")
    back_button.pack(pady=10, side="top", anchor="center")
    back_button.bind("<Enter>", lambda event: on_hover(event, back_button))
    back_button.bind("<Leave>", lambda event: on_leave(event, back_button))

# Initialize pygame mixer
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("music.mp3")

# Set the volume to 1.0 for maximum volume
pygame.mixer.music.set_volume(10.0)

pygame.mixer.music.play(-1)

root = tk.Tk()
root.title("Game Interface")
root.geometry("2000x2000")

try:
    # Load and set the background image using Pillow for JPG support
    bg_image = Image.open("skull.jpg")  # Replace with your actual file name
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to the image
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Error loading main background image:", str(e))

button_font = ("Arial", 12)

play_button = tk.Button(root, text="Play", command=choose_difficulty, font=button_font, height=2, width=15, bg="green")
play_button.pack(pady=20)
play_button.bind("<Enter>", lambda event: on_hover(event, play_button))
play_button.bind("<Leave>", lambda event: on_leave(event, play_button))

exit_button = tk.Button(root, text="Exit", command=exit_game, font=button_font, height=2, width=15, bg="green")
exit_button.pack(pady=20)
exit_button.bind("<Enter>", lambda event: on_hover(event, exit_button))
exit_button.bind("<Leave>", lambda event: on_leave(event, exit_button))

root.mainloop()

