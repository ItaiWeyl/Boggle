from boggle_board_randomizer import randomize_board
from ex11_utils import get_neighbors as neighbors


class Board:
    """this class represent a board of 4X4 of a random letters"""
    def __init__(self):
        self.size = 4
        self.table = randomize_board()

    def cell_list(self):
        """returns all the cell coordinates in the board"""
        cors_list = [(i, j) for i in range(len(self.table))
                     for j in range(len(self.table[i]))]
        return cors_list

    def get_letter(self, cor):
        """gets a coordinate, returns the letter on that cell in the voard"""
        cor_x = cor[0]
        cor_y = cor[1]
        if cor in self.cell_list():
            return self.table[cor_x][cor_y]
        else:
            return None

    def get_board(self):
        """returns the board list"""
        return self.table

    def get_size(self):
        """returns the size of the board"""
        return self.size

    def get_neighbors(self, cor):
        """returns the neighbors cells of a given cell in the board"""
        return neighbors(cor, self.table)

