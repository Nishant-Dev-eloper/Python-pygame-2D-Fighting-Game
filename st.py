import tkinter as tk
from tkinter import messagebox
import subprocess
import pygame
from PIL import Image, ImageTk

def run_game(difficulty):
    pygame.mixer.music.stop()
    process = subprocess.Popen(["python", "main.py", difficulty])
    process.wait()  # Wait for main.py process to finish
    root.deiconify()  # Bring back the game interface window

def exit_game():
    answer = messagebox.askquestion("Exit", "Do you really want to exit the game?")
    if answer == "yes":
        pygame.mixer.music.play()
        root.destroy()

def choose_difficulty():
    root.withdraw()  # Hide the game interface window
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("Choose Difficulty")
    difficulty_window.geometry("800x800")
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

    pygame.mixer.music.load("start_music.mp3")
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

    easy_button = tk.Button(difficulty_window, text="Easy", command=lambda: run_game_with_difficulty("easy"), bg="green", fg="white", font=button_font, height=2, width=15)
    easy_button.pack(pady=(20, 10), side="top", anchor="center")

    medium_button = tk.Button(difficulty_window, text="Medium", command=lambda: run_game_with_difficulty("medium"), bg="green", fg="white", font=button_font, height=2, width=15)
    medium_button.pack(pady=10, side="top", anchor="center")

    hard_button = tk.Button(difficulty_window, text="Hard", command=lambda: run_game_with_difficulty("hard"), bg="green", fg="white", font=button_font, height=2, width=15)
    hard_button.pack(pady=10, side="top", anchor="center")

    back_button = tk.Button(difficulty_window, text="Back", command=back_to_game_interface, bg="red", fg="white", font=button_font, height=2, width=15)
    back_button.pack(pady=10, side="top", anchor="center")

# Initialize pygame mixer
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("start_music.mp3")
pygame.mixer.music.play(-1)

root = tk.Tk()
root.title("Game Interface")
root.geometry("800x800")

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

play_button = tk.Button(root, text="Play", command=choose_difficulty, bg="green", fg="white", font=button_font, height=2, width=15)
play_button.pack(pady=20)

exit_button = tk.Button(root, text="Exit", command=exit_game, bg="green", fg="white", font=button_font, height=2, width=15)
exit_button.pack(pady=20)

root.mainloop()
