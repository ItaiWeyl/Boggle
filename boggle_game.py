from board import Board


######################################
TIME_LIMIT = 180
SECOND = 1
ZERO = 0
SCORE_CALC = 2
######################################


class BoggleGame:
    """
    this class is in charge of representing a game of boggle, with all the logical functions that runs the game
    """

    def __init__(self, words_dict):
        self.board = Board()
        self.current_word = ""
        self.path = []
        self.time = ZERO
        self.score = ZERO
        self.words_dict = words_dict
        self.words_found = []
        self.next_available = set(self.board.cell_list())
        self.game_over = False

    def get_current_word(self):
        """
        return the current word that written by far
        """
        return self.current_word

    def is_game_over(self):
        """
        returns True if the game is over, else False
        """
        return self.game_over

    def get_time(self):
        """
        returns the time that have passed
        """
        return self.time

    def add_second(self):
        """adds one second to the time, if time passed the time limit, changes the game to be over"""
        self.time += SECOND
        if self.time > TIME_LIMIT:
            self.game_over = True

    def update_score(self, score):
        """updates the score of the game """
        self.score = score

    def get_score(self):
        """returns the score of that game"""
        return self.score

    def get_available(self):
        """returns a set of all the coordinates that you can pick next for the path"""
        return self.next_available

    def next_cor_chosen(self, cor):
        """gets a coordinate to add to the current path, if it can be added to the path, updates the current word and
        updates the next_available set according to that coordinate and path then returns True. else returns false"""
        if cor in self.next_available or not self.next_available:
            self.current_word += self.board.get_letter(cor)
            self.path.append(cor)
            self.next_available = self.board.get_neighbors(cor) - set(self.path)
            return True
        return False

    def delete_word(self):
        """clears the path, current word and makes all cells to be available to pick"""
        self.path = []
        self.next_available = set(self.board.cell_list())
        self.current_word = ""

    def restart_game(self):
        """restart the values of the game in order to start a new game"""
        self.board = Board()
        self.score = ZERO
        self.time = ZERO
        self.words_found = []
        self.delete_word()
        self.game_over = False
        self.path = []
        self.next_available = set(self.board.cell_list())

    def is_word_legal(self):
        """checks if the current word is in the words dictionary and not already found, if it is new word that is in the
        dictionary, adds it to the words found list and updates the score and return True, else return false"""
        if self.current_word in self.words_dict and self.current_word not in self.words_found:
            self.words_found.append(self.current_word)
            self.score += len(self.path) ** SCORE_CALC
            self.delete_word()
            return True
        return False

    def get_path(self):
        """returns the current path"""
        return self.path

    def last_word_found(self):
        """returns the last word that was found"""
        return self.words_found[-1]

    def get_board_letter(self, cor):
        """gets a coordinate, returns the letter that in that spot on the board"""
        return self.board.get_letter(cor)

    def end_game(self):
        """ends the game"""
        self.game_over = True
