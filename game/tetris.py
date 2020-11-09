from game.board import Board, BoardShapeElement, BoardPrinter
from game.config import BOARD_SIZE
from game.shape import Shapes
from game.move import MoveDown, MOVE_LETTERS_CHOICES, MOVES_DICT, MoveInitial, MOVE_LETTERS_CHOICES_WITH_DESCRIPTION


class TetrisGame:
    """
    Class where main game flow occur
    """
    def __init__(self, board):
        self.board = board
        self.board_printer = BoardPrinter()
        self.shapes = Shapes()

    def start_game(self):

        while True:
            shape = self.shapes.get_random_shape()
            is_shape_move_possible, start_x = MoveInitial.can_move(self.board, shape)

            if not is_shape_move_possible:
                break

            board_shape_element = BoardShapeElement(shape, start_x=start_x, start_y=0)
            MoveInitial.move(self.board, board_shape_element)
            self.print_board(current_shape=board_shape_element)

            while self.board.has_shape_stuck_down(board_shape_element):  
                move_type = self.get_user_move() 
                self.board.put_shape_for_move(board_shape_element, move_type)
                self.print_board(current_shape=board_shape_element)
                if move_type is not MoveDown:
                    self.board.put_shape_for_move(board_shape_element, MoveDown)

        print("Game over")
        exit(0)

    def get_user_move(self):
        print("Enter your move choice. Available move choices: {}".format(MOVE_LETTERS_CHOICES_WITH_DESCRIPTION))
        while True:
            value = input()
            value_lower = value.lower()
            try:
                print("Selected move: {}".format(MOVES_DICT[value_lower].description))
                return MOVES_DICT[value]
            except KeyError:
                print("{} is not valid choice. Enter valid choice. Choices are: {}".format(value, str(MOVE_LETTERS_CHOICES)))

    def print_board(self, current_shape):
        self.board_printer.print_board(self.board, current_shape=current_shape)

class Tetris:

    def __init__(self):
        self.initialize_board()

    def initialize_board(self):
        self.board = Board(BOARD_SIZE)

    def start_game(self):
        game = TetrisGame(board=self.board)
        game.start_game()


