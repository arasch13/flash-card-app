# import catch as catch
import pandas
from tkinter import *
import random
import os


BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "ARIAL"
TIMER_SEC = 5


# ---------------------------- DICT SETUP ------------------------------- #
# load dictionary with word to learn
def load_dict():
    try:
        dictionary = pandas.read_csv("./data/words_to_learn.csv")
    except FileNotFoundError:
        dictionary = pandas.read_csv("./data/french_words.csv")
        dictionary.to_csv("./data/words_to_learn.csv")
    finally:
        vocabulary_dict = dictionary.to_dict(orient='records')
    return vocabulary_dict


def random_word():
    """dictionary as Pandas DataFrame
    returns french and english word"""
    global vocabulary_dict
    try:
        random_entry = vocabulary_dict[random.randint(0, len(vocabulary_dict)-1)]
    except ValueError:
        os.remove("./data/words_to_learn.csv")
        vocabulary_dict = load_dict()
        random_word()
        return 0
    else:
        return random_entry

vocabulary_dict = load_dict()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def start_timer():
    count_down(TIMER_SEC)

def count_down(count):
    global timer
    flashcard.itemconfig(timer_text, text=f"00:0{count}", fill="grey")
    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        flip_card()
        window.after_cancel(timer)


# ---------------------------- UI SETUP ------------------------------- #

def next_word():
    global random_entry
    random_entry = random_word()
    french_word = random_entry["French"]
    flashcard.itemconfig(body, image=flashcard_front_image)
    flashcard.itemconfig(title_text, text="French", fill="black")
    flashcard.itemconfig(word_text, text=french_word, fill="black")
    confirm_button.config(state="disabled")
    cancel_button.config(state="disabled")
    start_timer()


def flip_card():
    flashcard.itemconfig(body, image=flashcard_back_image)
    flashcard.itemconfig(title_text, text="English", fill="white")
    english_word = random_entry["English"]
    flashcard.itemconfig(word_text, text=english_word, fill="white")
    flashcard.itemconfig(timer_text, text="")
    confirm_button.config(state="active")
    cancel_button.config(state="active")


def correct_answer():
    global vocabulary_dict
    vocabulary_dict.remove(random_entry)
    new_data = pandas.DataFrame(vocabulary_dict)
    new_data.to_csv("./data/words_to_learn.csv", index=False)
    next_word()


# create window
window = Tk()
window.title("Flash Card App")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# load UI images
flashcard_front_image = PhotoImage(file="./images/card_front.png")
flashcard_back_image = PhotoImage(file="./images/card_back.png")
confirm_image = PhotoImage(file="./images/right.png")
cancel_image = PhotoImage(file="./images/wrong.png")

# show flash card
flashcard = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
body = flashcard.create_image(400, 263, image=flashcard_front_image)
title_text = flashcard.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
word_text = flashcard.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
timer_text = flashcard.create_text(700, 50, text="", font=(FONT_NAME, 30, "bold"))
flashcard.grid(column=0, row=0, columnspan=2)

# create buttons
confirm_button = Button(image=confirm_image, highlightthickness=0, command=correct_answer, state="disabled")
confirm_button.grid(column=0, row=1)
cancel_button = Button(image=cancel_image, highlightthickness=0, command=next_word, state="disabled")
cancel_button.grid(column=1, row=1)

next_word()

# hold window
window.mainloop()