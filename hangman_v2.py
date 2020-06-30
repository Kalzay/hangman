import os
import pickle
import random
from time import sleep


# Hangman is a classic childhood game


### FUNCTIONS ###

def header():
    os.system('clear')

    print("\t**************************************")
    print("\t*************  Hangman!  *************")
    print("\t**************************************")


def display_bar(display, lives, current_body, guessed):
    # Displays lives remaining, letters guessed, hanging man and word progress
    print('\t\t Lives remaining: %s' % lives)
    print('\t\t Guessed:', ', '.join(str(x).upper() for x in guessed))
    man(lives, current_body)
    print('\t\t ___________________')
    print('\t\t %s               \ |' % current_body[0])
    print('\t\t %s                \|' % current_body[1])
    print('\t\t%s%s%s               |' % (current_body[3], current_body[2], current_body[4]))
    print('\t\t %s                 |' % current_body[5])
    print('\t\t%s%s               |' % (current_body[6], current_body[7]))
    print('\t\t                  /|')
    print('\t\t                 / |')
    print('\t\t -------------------')
    print(display)


def load_words():
    # Loads stored words.
    try:
        file_object = open('words.pydata', 'rb')
        words = pickle.load(file_object)
        file_object.close()
        return words
    except Exception as e:
        print(e)
        return []


def get_new_word():
    # Asks the user for a new word, and stores the word if we don't already know it.
    header()
    new_word = input("\nPlease tell me a new word (or type q to quit): ")
    if new_word == 'q':
        return
    elif new_word in words:
        print("\nI already know the word %s" % new_word.upper())
    else:
        words.append(new_word)
        print("\nThank you for this new word: %s" % new_word.upper())
        save()
    sleep(3)


def show_words():
    header()
    print('\nThese are the words I know:')
    print(', '.join(str(x).upper() for x in words))


def save():
    # This function dumps the words into a file, and prints a save message.
    try:
        file_object = open('words.pydata', 'wb')
        pickle.dump(words, file_object)
        file_object.close()
        print("\nI will remember this new word.")
    except Exception as e:
        print("\nI won't be able this new word. Please try again.")
        print(e)


def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Play Hangman with random word.")
    print("[2] Play Hangman with chosen word.")
    print("[3] Enter a new word for Hangman.")
    print('[4] View stored words.')
    print("[q] Quit.\n")

    return input("What would you like to do? ")


def correct_guess(word, display, letter):
    # Uses zip to pair word letters with current display.
    #  Constructs new display with previous display.
    new_display = ''
    for w, l in zip(word, display):
        if letter.lower() == w:
            new_display += letter.upper()
        else:
            new_display += l
    display = new_display
    return display


def man(lives, current_body):
    # Constructs a hanging man incrementally depending on number of failed guesses
    full_body = ['|', 'O', '|', '/', '\ ', '|', '/', ' \ ']
    for i in range(0, len(full_body) - lives):
        current_body[i] = full_body[i]
    return current_body


def main(word):
    # Initial settings. Empty body, lives, starting display.
    current_body = [' ', ' ', ' ', ' ', '  ', ' ', ' ', '   ']
    lives = len(current_body)
    display = '_' * len(word)
    letter = ''
    guessed = []

    header()
    display_bar(display, lives, current_body, guessed)
    while letter != 'quit':

        letter = input("Guess a letter (or type quit to exit to main menu): ")
        if letter == 'quit':
            # Checks if the player wants to quit.
            header()
            display_bar(display, lives, current_body, guessed)
            print('Thanks for playing!')
            sleep(3)
        elif len(letter) > 1:
            # Checks if player has entered a valid guess.
            header()
            display_bar(display, lives, current_body, guessed)
            print('Not a valid guess, try again.')
        elif letter in word:
            # Checks if guess was correct. Updates display.
            if letter not in guessed:
                guessed.append(letter)
                display = correct_guess(word, display, letter)
                header()
                display_bar(display, lives, current_body, guessed)
                print('Good guess!')
            else:
                header()
                display_bar(display, lives, current_body, guessed)
                print('You already guessed that letter!')
            # Check if the player has won.
            if '_' not in display:
                header()
                display_bar(display, lives, current_body, guessed)
                print('Congratulations, you won!')
                sleep(3)
                break
        else:
            # Removes a life. Checks if player has lost. Updates display
            if letter not in guessed:
                guessed.append(letter)
                lives -= 1
                if lives == 0:
                    # Shows full word when player loses
                    header()
                    display_bar(word.upper(), lives, current_body, guessed)
                    print('Game over!')
                    sleep(3)
                    break
                else:
                    header()
                    display_bar(display, lives, current_body, guessed)
                    print('Unlucky')
            else:
                header()
                display_bar(display, lives, current_body, guessed)
                print('You already guessed that letter!')


### MAIN PROGRAM ###
choice = ''
words = load_words()

while choice != 'q':
    header()
    print('Welcome to Hangman! Please select an option:')
    choice = get_user_choice()

    if choice == '1':
        word = random.choice(words)
        main(word)
    elif choice == '2':
        header()
        word = input('Please enter a word: ')
        main(word)
    elif choice == '3':
        get_new_word()
    elif choice == '4':
        show_words()
        input("Press Enter to continue...")
    elif choice == 'q':
        header()
        print('Goodbye!')
    else:
        header()
        print("I don't understand that choice.")
