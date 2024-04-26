from typing import List, Tuple, Iterable, Optional, Dict


Board = List[List[str]]
Path = List[Tuple[int, int]]


def get_words_dict(address):
    words_dict = {}
    with open(address, "r") as file:
        for word in file:
            words_dict[word.strip()] = "_"
    return words_dict


def sort_by_letters(board: Board, words: Iterable[str]) -> Dict[str, str]:
    """ This function gets a 2-dim list (board) and an iterable with words, filters all the words from the iterable that
    contains letters who don't appear in the board. returns a sorted dictionary with the relevant words"""
    sorted_dict = {}
    one_len_letters = []
    two_len_letters = []

    # adding all the letters in the board to a string
    for line in board:
        for letter in line:
            if len(letter) == 1:
                one_len_letters.append(letter)
            else:
                two_len_letters.append(letter)
    for word in words:
        for i in range(len(word)):
            if word[i] not in one_len_letters:
                if len(word) == 1:
                    break
                else:
                    if i == 0:
                        if word[0:2] not in two_len_letters:
                            break
                    elif i == len(word) - 1:
                        if word[-2:] not in two_len_letters:
                            break
                    else:
                        if (word[i - 1: i + 1] not in two_len_letters) and (word[i: i + 2] not in two_len_letters):
                            break
        else:
            sorted_dict[word] = "_"
    return sorted_dict


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """ This function checks the validity of a given path on the board. It verifies that the path follows neighboring
        positions on the board, stays within the boundaries of the board, and forms a valid word from the provided
        iterable of words."""
    board_length = len(board)
    board_width = len(board[0])
    path_set = set(path)
    if not path or not words:
        return None
    if len(path) != len(path_set):  # in case one of the coordinates appears twice in the path
        return None

    for i in range(len(path) - 1):   # verify that each coordinate in the path is a neighbor of the next one
        cor = path[i]
        next_cor = path[i+1]
        delta_cor_x = cor[0] - next_cor[0]
        delta_cor_y = cor[1] - next_cor[1]
        if (delta_cor_x > 1 or delta_cor_x < -1) or (delta_cor_y > 1 or delta_cor_y < -1):
            return None
        # in case one of the coordinates is outside the board
        if cor[0] >= board_length or cor[0] < 0 or cor[1] >= board_width or cor[1] < 0:
            return None

    if path[-1][0] >= board_length or path[-1][0] < 0 or path[-1][1] >= board_width or\
            path[-1][1] < 0:  # for the last coordinate
        return None

    word = path_to_word(board, path)  # check if the word is in the dictionary
    if word in words:
        return word
    else:
        return None


def path_to_word(board, path):
    """ gets a path and a board, creates the word from that path on the board"""
    word = ""
    for cor in path:
        word += board[cor[0]][cor[1]]
    return word


def get_neighbors(cor, board):
    """ gets a coordinate, returns a list with all its neighbors"""
    neighbors = set()
    cor_row = cor[0]
    cor_col = cor[1]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= cor_row + i < len(board) and 0 <= cor_col + j < len(board[0]):
                new_cor = (cor_row + i, cor_col + j)
                if new_cor != cor:
                    neighbors.add(new_cor)
    return neighbors


def is_path_in_words(words_dict, path_word, illegal_dict):
    """ Checks if the current part of the word is relevant. if none of the words in the dictionary contains the sequence
    that the path represents, the functions add the sequence to the illegal dictionary """
    for word in words_dict:
        if path_word in word:
            return True
    illegal_dict[path_word] = ""
    return False


def find_len_path_helper(n, board, words_dict, final_list, path, illegal_words):
    path_word = path_to_word(board, path)
    if len(path) == n:
        if path_word not in illegal_words:
            if is_path_in_words(words_dict, path_word, illegal_words):
                if path_word in words_dict:
                    final_list.append(path)
        return None
    if path_word in illegal_words:  # if the current sequence of letter is not relevant, we can stop
        return None
    if is_path_in_words(words_dict, path_word, illegal_words):
        path_set = set(path)
        neighbors = get_neighbors(path[-1], board)
        neighbors = neighbors - path_set
        for cor in neighbors:
            find_len_path_helper(n, board, words_dict, final_list, path + [cor], illegal_words)
    return None


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """his function finds paths of length n on the board that form valid words from the given iterable of words.
        It returns a list of these paths. It utilizes a recursive helper function to explore the board and adds valid
        paths to the final list."""
    final_list = []
    if n == 0:
        return final_list
    words_dict = {}
    for word in words:
        if len(word) >= n:
            words_dict[word] = "_"
    words_dict = sort_by_letters(board, words_dict)
    illegal_words = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            cor = (i, j)
            find_len_path_helper(n, board, words_dict, final_list, [cor], illegal_words)
    return final_list


def find_len_words_helper(n, board, words_dict, final_list, path, illegal_words):
    path_word = path_to_word(board, path)
    if len(path_word) == n:
        if path_word not in illegal_words:
            if is_path_in_words(words_dict, path_word, illegal_words):
                if path_word in words_dict:
                    final_list.append(path)
        return None
    if path_word in illegal_words:
        return None
    if is_path_in_words(words_dict, path_word, illegal_words):
        path_set = set(path)
        neighbors = get_neighbors(path[-1], board)
        neighbors = neighbors - path_set
        for cor in neighbors:
            find_len_words_helper(n, board, words_dict, final_list, path + [cor], illegal_words)
    return None


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """This function finds paths on the board that form words of length n from the given iterable of words. It
          returns a list of these paths. The function utilizes a recursive helper function to explore the board and
          add valid paths to the final list."""
    final_list = []
    if n == 0:
        return final_list
    words_dict = {}
    for word in words:
        if len(word) == n:
            words_dict[word] = "_"
    words_dict = sort_by_letters(board, words_dict)
    illegal_words = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            cor = (i, j)
            find_len_words_helper(n, board, words_dict, final_list, [cor], illegal_words)
    return final_list


def max_score_helper(board, words_dict, final_dict, path, illegal_words):
    path_word = path_to_word(board, path)
    if path_word in illegal_words:
        return None
    if path_word in words_dict:
        if path_word not in final_dict:
            final_dict[path_word] = (path, len(path) ** 2)
        else:
            new_score = len(path) ** 2
            previous_score = final_dict[path_word][1]
            if new_score > previous_score:  # if word already in the final dict, check if this path gives higher score
                final_dict[path_word] = (path, new_score)
    if is_path_in_words(words_dict, path_word, illegal_words):
        path_set = set(path)
        neighbors = get_neighbors(path[-1], board)
        neighbors = neighbors - path_set
        for cor in neighbors:
            max_score_helper(board, words_dict, final_dict, path + [cor], illegal_words)
    return None


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """This function finds the  highest-scoring path for each word in the board returns them as a list. It recursively
        explores the board, updates a dictionary with paths and scores, and extracts the high-scoring paths for the
        final list."""
    final_list = []
    final_dict = {}
    words_dict = {}
    for word in words:
        words_dict[word] = "_"
    words_dict = sort_by_letters(board, words_dict)
    illegal_words = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            cor = (i, j)
            max_score_helper(board, words_dict, final_dict, [cor], illegal_words)
    for value in final_dict.values():
        final_list.append(value[0])
    return final_list
