from typing import Union

import numpy as np

from game.config import BOARD_SIZE
from game.move import MoveDown
from game.shape import Shapes, ShapeElement


class BoardShapeElement(ShapeElement):
    """
    Class that represents given ShapeElement that is currently moving on the board.
    So we can refer to it element and move it depends on specific Move
    """

    def __init__(self, shape, start_x, start_y):
        super().__init__(shape)
        self.shape = shape
        self.start_x = start_x
        self.start_y = start_y
        self.cells = []

    @property
    def position(self):
        return (self.start_x, self.start_y)

    def get_size(self) -> Union[int, int]:
        return self.shape.get_size()

    def get_size_x(self) -> int:
        return self.shape.get_size_x()

    def get_size_y(self) -> int:
        return self.shape.get_size_y()

    def set_start_x(self, x):
        self.start_x = x

    def set_start_y(self, y):
        self.start_y = y

    def save_filled_board_cells(self, board_cells):
        self.cells = board_cells

    def get_cells(self):
        return self.cells

    def get_cells_from_right_order(self) -> list:
        return sorted(self.cells, key=lambda obj: obj.x, reverse=True)

    def get_cells_from_left_order(self) -> list:
        return sorted(self.cells, key=lambda obj: obj.x, reverse=False)

    def get_cells_from_bottom_order(self) -> list:
        return sorted(self.cells, key=lambda obj: obj.y, reverse=True)


class Board:

    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.shapes = Shapes()
        self.board_cells = {}
        self.initialize_board_cells()

    def is_space_for_shape(self, start_x, shape: ShapeElement) -> bool:
        for y, row in enumerate(shape.current_shape_array):
            for x, value in enumerate(row):
                if value == 1:
                    if self.get_value_for_coordinates(start_x+x, y).is_filled():
                        return False
        return True

    def put_shape_for_move(self, board_shape_element, move_type):
        if move_type.can_move(board=self, shape=board_shape_element):
            move_type.move(board=self, shape=board_shape_element)

    def has_shape_stuck_bottom(self, board_shape_element: BoardShapeElement) -> bool:
        """
        Get know if current BoardShapeElement is able to move down
        or it reach the bottom
        """
        return MoveDown.can_move(self, board_shape_element)

    def initialize_board_cells(self):
        for y in range(self.size):
            for x in range(self.size):
                coordinates = (x, y)
                self.board_cells[coordinates] = BoardCell(self, x, y, filled=False)

    def get_value_for_coordinates(self, x, y) -> 'BoardCell':
        # sorry for this hack but I know it once occurred somewhere
        # but it was never found later.
        if x >= self.size_board:
            x = self.size_board
        if y >= self.size_board:
            y = self.size_board

        return self.board_cells[(x, y)]

    def set_board_cell_filled_by_object(self, x, y, filled_object):
        self.get_value_for_coordinates(x, y).set_filled_by_object(filled_object)

    @property
    def size_board(self):
        """
        Used to define size board to not cross border.
        Because first index == 0, last index == 19. Sum of cells: self.size==20
        """
        return self.size - 1


class BoardPrinter:
    """
    Class for printing existing state of board.
    We distint three states:
    0 - not filled BoardCell
    1 - filled BoardCell
    2 - BoardCell filled by currently moving BoardShapeElement
    """

    @classmethod
    def print_board(cls, board, current_shape):
        matrix = np.zeros((board.size, board.size), int)

        for x in range(board.size):
            for y in range(board.size):
                coordinates = (y, x)
                matrix[coordinates] = board.get_value_for_coordinates(x, y).is_filled()

        for cell in current_shape.cells:
            coordinates = (cell.y, cell.x)
            matrix[coordinates] = 2

        print(matrix)


class BoardCell:
    """
    Single Board's Cell representation.
    """
    def __init__(self, board=None, x=0, y=0, filled=False):
        self.board = board
        self.x = x
        self.y = y
        self.filled = filled
        self.filled_by_object = None

    def remove_filled_by_object(self):
        self.filled_by_object = None
        self.set_unfilled()

    def set_filled_by_object(self, obj):
        self.filled_by_object = obj
        self.set_filled()

    def set_filled(self):
        self.filled = True

    def set_unfilled(self):
        self.filled = False

    def is_filled(self):
        return int(self.filled)

    def __str__(self):
        return int(self.is_filled())

    def __repr__(self):
        return str(int(self.is_filled()))


