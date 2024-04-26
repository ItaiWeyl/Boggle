import tkinter as tk
import ex11_utils as helper
import time
from boggle_game import BoggleGame
from PIL import ImageTk, Image
from GUI_globals import *


class BoggleGUI:
    """The constructor method that initializes the Boggle game GUI. It sets up the game window,
        labels, buttons, and images."""
    def __init__(self, root, game):
        self.game = game
        self.root = root
        root.configure(bg=BG_COLOR)
        root.title(TITLE)
        root.resizable(False, False)
        self.height = BOARD_SIZE
        self.screen_labels = []
        self.width = BOARD_SIZE
        self.last_word_loc = [FIRST_WORD_X, FIRST_WORD_Y]
        self.buttons = []
        self.words_labels = []
        self.first_word = True

        # set delete label
        self.delete_button = tk.Button(self.root, text=DELETE_TXT, width=5, height=4, fg=RED)
        self.delete_button.config(command=lambda: self.delete_word())
        # set the current word display
        self.word_display = tk.Label(self.root, text=self.game.get_current_word(), font=(WORD_FONT, FONT20), fg=BLACK,
                                     bg=BG_COLOR, width=len(self.game.get_current_word()))
        # set timer label
        self.timer = tk.Label(self.root, text=START_TIME, font=(FUNC_FONT, 25), fg=RED, bg=WHITE, width=10)
        self.timer.config(borderwidth=2, relief=tk.SOLID)
        # set options menu label
        self.restart_var = tk.StringVar()
        self.restart_var.set(OPTIONS)
        self.options = tk.OptionMenu(self.root, self.restart_var, END_GAME, command=self.end_game)
        self.options.config(highlightcolor=BLACK, highlightbackground=BLACK)
        # set words found title label
        self.words_title = tk.Label(self.root, text=WORDS_FOUND, font=(MENU_FONT, FONT20, UNDER_LINE), bg=BG_COLOR)
        # set score label
        self.score_label = tk.Label(self.root, text=SCORE_TXT + str(self.game.get_score()), fg=BLACK,
                                    font=(MENU_FONT, FONT20), bg=BG_COLOR)
        # set the welcome screen
        self.start_label = tk.Label(root, width=200, height=84, bg=BG_COLOR)  # background color of the welcome screen

        # set images labels
        image = Image.open(IMAGE1)
        tk_image = ImageTk.PhotoImage(image)
        self.start_image = tk.Label(root, image=tk_image)
        self.start_image.image = tk_image
        image2 = Image.open(IMAGE2)
        tk_image2 = ImageTk.PhotoImage(image2)
        self.game_image = tk.Label(self.root, image=tk_image2, background=BG_COLOR)
        self.game_image.image = tk_image2

        # set the welcome screen
        self.start_image.place(x=-100, y=60)
        self.start_label.place(x=ZERO, y=ZERO)
        self.start_button = tk.Button(root, text=START_GAME, width=15, height=4, font=(MENU_FONT, FONT20),
                                      command=self.start_game, fg=RED, bg=GOLD)
        self.start_button.place(x=370, y=350)
        self.screen_labels.append(self.start_label)
        self.screen_labels.append(self.start_button)
        self.screen_labels.append(self.start_image)

    def update_words_labels(self, word):
        """  Updates the labels displaying the current word picked."""
        new_label = tk.Label(self.root, text=word, font=(FUNC_FONT, FONT12), fg=BLACK, bg=BG_COLOR)
        self.words_labels.append(new_label)
        prev_x = self.last_word_loc[0]
        prev_y = self.last_word_loc[1]
        if prev_x == FIRST_WORD_X and prev_y == FIRST_WORD_Y and self.first_word:
            new_label.place(x=FIRST_WORD_X, y=FIRST_WORD_Y)
            self.last_word_loc = [prev_x, prev_y]
            self.first_word = False
        elif prev_y == LAST_LINE:
            self.last_word_loc = [prev_x + X_GAP, FIRST_WORD_Y]
            new_label.place(x=prev_x + X_GAP, y=FIRST_WORD_Y)
        else:
            new_label.place(x=prev_x, y=prev_y+Y_GAP)
            self.last_word_loc = [prev_x, prev_y + Y_GAP]

    def button_press(self, row, col):
        """ Handles the button press event for the game buttons. Checks if the word is legal. Calls the
            update_button_color and the update_words_label functions."""
        if self.game.next_cor_chosen((row, col)):
            self.word_display.configure(text=self.game.get_current_word())
            if self.game.is_word_legal():
                time.sleep(0.5)
                self.word_display.configure(text=self.game.get_current_word())
                self.score_label.configure(text=SCORE_TXT + str(self.game.get_score()))
                self.update_words_labels(self.game.last_word_found())
            self.update_buttons_color()

    def delete_word(self):
        """ Deletes the current word formed from the display """
        self.game.delete_word()
        self.word_display.configure(text=self.game.get_current_word())
        self.update_buttons_color()

    def set_buttons(self):
        """  Sets up the game buttons on the GUI. Adds all buttons objects to the self_buttons attribute for
            later use"""
        self.buttons = []
        start_col = FIRST_BUTTON_ROW
        start_row = FIRST_BUTTON_COL
        for row in range(self.height):
            tmp_row = []
            for col in range(self.width):
                new_b = tk.Button(self.root, text=self.game.get_board_letter((row, col)), width=5, height=5)
                new_b.config(command=lambda r=row, c=col: self.button_press(r, c))
                new_b.place(x=start_col + row * 100, y=start_row + col * 100)
                tmp_row.append(new_b)
            self.buttons.append(tmp_row)

    def update_buttons_color(self):
        """ Updates the colors of the game buttons based on the current path and available positions on the game
            board."""
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons[0])):
                button = self.buttons[row][col]
                if self.game.get_path():
                    if (row, col) in self.game.get_path():
                        button.config(bg=PATH_COLOR)
                    elif (row, col) in self.game.get_available():
                        button.config(bg=AVAILABLE_COLOR)
                    else:
                        button.config(bg=BUTTON_COLOR)
                else:
                    button.config(bg=BUTTON_COLOR)

    def update_time(self):
        """ starts the countdown timer, updates the time that have passed in the game and updates the label that
            shows the timer to show the current time by the format minutes:seconds. calls itself every second so
            the timer will run properly """
        self.game.add_second()
        seconds = TIME_LIMIT - self.game.get_time()
        minutes = ZERO
        while seconds >= MINUTE:
            seconds -= MINUTE
            minutes += ONE
        time_display = str(minutes) + CLOCK + str(seconds)
        self.timer.configure(text=time_display)
        if self.game.is_game_over():
            self.end_game_window()
            return None
        self.timer.after(1000, self.update_time)

    def start_game(self):
        """ The start_game method clears the screen, places the game elements such as the image, word display, buttons,
            timer, options menu, and score label at their respective positions, and restarts the game while setting
            the first_word flag to True."""
        self.clear_screen()
        self.game_image.place(x=ZERO, y=400)
        self.word_display.place(x=400, y=30)
        self.delete_button.place(x=180, y=150)
        self.timer.place(x=380, y=70)
        self.options.place(x=10, y=10)
        self.score_label.configure(text=SCORE_TXT + str(self.game.get_score()))
        self.score_label.place(x=180, y=70)
        self.words_title.place(x=720, y=70)
        self.first_word = True
        self.game.restart_game()
        self.set_buttons()
        self.update_time()
        self.last_word_loc = (FIRST_WORD_X, FIRST_WORD_Y)

    def delete_words_on_screen(self):
        for label in self.words_labels:
            label.destroy()
        self.words_labels = []

    def end_game_window(self):
        """ Displays the end game window in the GUI, showing the "Game Over" message, final score, and an option to
            play again. It clears the screen, creates labels and buttons for the end game window, and handles the
            restart game functionality."""
        end_background_label = tk.Label(self.root, width=200, height=84, bg=BG_COLOR)
        end_text = tk.Label(self.root, text=GAME_OVER, font=(MENU_FONT, FONT40), bg=BG_COLOR)
        play_again_button = tk.Button(self.root, text=PLAY_AGAIN, width=15, height=4, font=(MENU_FONT, FONT20),
                                      command=self.start_game, fg=RED, bg=GOLD)
        final_score_label = tk.Label(self.root, text=FINAL_SCORE_MESSAGE + str(self.game.get_score()),
                                     font=(WORD_FONT, FONT20), bg=BG_COLOR)
        final_score_label.place(x=345, y=150)
        end_text.place(x=320, y=60)
        end_background_label.place(x=ZERO, y=ZERO)
        play_again_button.place(x=370, y=350)
        self.screen_labels.append(final_score_label)
        self.screen_labels.append(end_background_label)
        self.screen_labels.append(play_again_button)
        self.screen_labels.append(end_text)
        self.game.restart_game()
        self.word_display.configure(text=self.game.get_current_word())
        self.delete_words_on_screen()

    def end_game(self, optional):
        self.restart_var.set(OPTIONS)
        self.game.end_game()

    def clear_screen(self):
        """ Clears the screen by destroying all the GUI elements."""
        for item in self.screen_labels:
            item.destroy()
        self.screen_labels = []


if __name__ == '__main__':
    new_root = tk.Tk()
    words = helper.get_words_dict(WORDS_DICT_PATH)
    new_root.geometry(WINDOW_SIZE)
    new_game = BoggleGame(words)
    GUI = BoggleGUI(new_root, new_game)
    new_root.mainloop()
