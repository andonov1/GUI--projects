import random
from tkinter import *
from string import ascii_uppercase
from tkinter import messagebox

window = Tk()
window.title('Hangman')

words_list = ['HELLO', 'ELEPHANT', 'PLANET', 'OCEAN', 'DOG', 'ORANGE', 'HIGHWAY', 'ROAD', 'LAPTOP', 'COMPUTER',
              'SPEAKERS', 'HEADPHONES', 'KEYBOARD', 'DOOR', 'GLASS', 'ENERGY', 'MACHINE', 'NOTEBOOK', 'PAPER',
              'STORM', 'SNACKS', 'SPINACH', 'SPIRAL', 'TRAIN', 'TRANSLATE', 'BAKE', 'STRANGE', 'STANDARD', 'TOGETHER',
              'PRODUCT']

photos = [PhotoImage(file="/home/nikolay/Desktop/hangman/1.png"),
          PhotoImage(file="/home/nikolay/Desktop/hangman/2.png"), PhotoImage(
        file="/home/nikolay/Desktop/hangman/3.png"), PhotoImage(file="/home/nikolay/Desktop/hangman/4.png"), PhotoImage(
        file="/home/nikolay/Desktop/hangman/5.png"), PhotoImage(file="/home/nikolay/Desktop/hangman/6.png"), PhotoImage(
        file="/home/nikolay/Desktop/hangman/7.png")]


def new_game():
    global word_with_spaces
    global cnt_guesses
    global current_word
    cnt_guesses = 0
    imgLabel.config(image=photos[0])

    current_word = random.choice(words_list)
    word_with_spaces = " ".join(current_word)
    lblWord.set((" ".join("_" * len(current_word))))


def guess(letter):
    global cnt_guesses
    if cnt_guesses < 11:
        txt = list(word_with_spaces)
        guessed = list(lblWord.get())
        if word_with_spaces.count(letter) > 0:
            for i in range(len(txt)):
                if txt[i] == letter:
                    guessed[i] = letter
                lblWord.set("".join(guessed))
                if lblWord.get() == word_with_spaces:
                    messagebox.showinfo('Hangman', "You found the word!")
                    new_game()
        else:
            cnt_guesses += 1
            imgLabel.config(image=photos[cnt_guesses])
            if cnt_guesses == 6:
                message = f'Game Over! \nThe correct word was: {current_word}'
                messagebox.showwarning('Hangman', message)


imgLabel = Label(window)
imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)
imgLabel.config(image=photos[0])

lblWord = StringVar()
Label(window, textvariable=lblWord, font=('Arial', 40, 'bold')).grid(row=0, column=2, columnspan=6, padx=10)

# input letters
n = 0
for c in ascii_uppercase:
    Button(window, text=c, command=lambda c=c: guess(c), font=('Arial', 20), width=11).grid(row=1 + n // 9,
                                                                                            column=n % 9)
    n += 1

Button(window, text='New Game', command=new_game, font=('Arial', 25, 'bold')).grid(row=3, column=8)
window.mainloop()
