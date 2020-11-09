from game.coordinates import Coordinates
from game.shape import ShapeElement


class Move:
    """
    Base class of each Move
    """
    letter = None
    description = ""

    @classmethod
    def move(cls, board, shape):
        raise NotImplementedError

    @classmethod
    def can_move(cls, board, shape):
        raise NotImplementedError


class MoveInitial(Move):
    """
    Class for Initial Move that is already appeared on the board
    """

    @classmethod
    def move(cls, board, shape):
        board_shape_current_x = shape.start_x
        board_shape_current_y = shape.start_y

        filled_board_cells = []

        for x in range(shape.shape.get_size_x()):
            for y in range(shape.shape.get_size_y()):

                if shape.shape.current_shape_array[(y, x)] == 1:
                    filled_board_cells.append(
                        board.get_value_for_coordinates(
                            x=board_shape_current_x+x,
                            y=board_shape_current_y+y
                        )
                    )
                    board.set_board_cell_filled_by_object(
                        x=board_shape_current_x + x,
                        y=board_shape_current_y + y,
                        filled_object=shape,
                    )
        shape.save_filled_board_cells(filled_board_cells)

    @classmethod
    def can_move(cls, board, shape: ShapeElement = None):

        start_x = 0
        for x in range(start_x, board.size_board):
            is_space_for_shape = board.is_space_for_shape(
                start_x=x,
                shape=shape
            )
            if is_space_for_shape:
                return True, x
        return False, None


class MoveLeft(Move):
    letter = 'a'
    description = "Move left"

    @classmethod
    def move(cls, board, shape):
        shape.switchd_shape_size = False
        new_start_x, new_start_y = shape.start_x - 1, shape.start_y

        cells_order_from_right = shape.get_cells_from_left_order()
        new_cells = []
        for board_cell in cells_order_from_right:
            board_cell_successor_x = board_cell.x - 1
            board_cell_successor_y = board_cell.y
            board_cell_successor = board.get_value_for_coordinates(
                x=board_cell_successor_x,
                y=board_cell_successor_y
            )
            board.set_board_cell_filled_by_object(
                x=board_cell_successor_x,
                y=board_cell_successor_y,
                filled_object=board_cell_successor
            )
            new_cells.append(board_cell_successor)
            board_cell.remove_filled_by_object()
        shape.save_filled_board_cells(new_cells)
        shape.set_start_x(new_start_x)
        shape.set_start_y(new_start_y)

    @classmethod
    def can_move(cls, board, shape):

        if shape.start_x == 0:
           return False

        size_y = shape.get_size_y()
        shape_cells = shape.get_cells_from_left_order()
        cell_most_left = shape_cells[0]

        x = cell_most_left.x - 1
        for y in range(shape.start_y, shape.start_y+size_y):
            if board.get_value_for_coordinates(
                x=x,
                y=y
            ).is_filled():
                return False

        return True


class MoveRight(Move):
    letter = 'd'
    description = "Move right"

    @classmethod
    def move(cls, board, shape):
        new_start_x, new_start_y = shape.start_x+1, shape.start_y

        cells_order_from_right = shape.get_cells_from_right_order()
        new_cells = []
        for board_cell in cells_order_from_right:
            board_cell_successor_x = board_cell.x+1
            board_cell_successor_y = board_cell.y
            board_cell_successor = board.get_value_for_coordinates(
                x=board_cell_successor_x,
                y=board_cell_successor_y
            )
            board.set_board_cell_filled_by_object(
                x=board_cell_successor_x,
                y=board_cell_successor_y,
                filled_object=board_cell_successor
            )
            new_cells.append(board_cell_successor)
            board_cell.remove_filled_by_object()
        shape.save_filled_board_cells(new_cells)
        shape.set_start_x(new_start_x)
        shape.set_start_y(new_start_y)

    @classmethod
    def can_move(cls, board, shape):
        size_x = shape.get_size_x()
        size_y = shape.get_size_y()
        if shape.start_x+size_x > board.size_board:
            return False

        shape_cells = shape.get_cells_from_right_order()
        cell_most_right = shape_cells[0]
        x = cell_most_right.x + 1

        for y in range(shape.start_y, shape.start_y+size_y):
            if board.get_value_for_coordinates(
                    x=x,
                    y=y
            ).is_filled():
                return False

        return True


class MoveRotation(Move):

    @classmethod
    def move(cls, board, shape):
        raise NotImplementedError

    @classmethod
    def can_move(cls, board, shape):
        size_y = shape.get_size_y()
        shape_y_position = shape.start_y + size_y

        if shape_y_position > board.size_board:
            return False

        if board.get_value_for_coordinates(
                x=shape.start_x,
                y=shape_y_position
        ).is_filled():
            return False

        return True


class MoveClockwise(MoveRotation):
    letter = 'w'
    description = "Move clockwise"

    @classmethod
    def move(self, board, shape):
        shape_start_x, shape_start_y = shape.start_x, shape.start_y
        shape.rotate_clockwise()

        new_cells = []

        for y, row in enumerate(shape.current_shape.current_shape_array):
            for x, value in enumerate(row):
                if value == 1:
                    new_cells.append(
                        Coordinates(x=shape_start_x+x, y=shape_start_y+y)
                    )

        previous_cells = shape.get_cells()
        for board_cell in previous_cells:
            board_cell.remove_filled_by_object()

        new_cells_objects = []
        for cell in new_cells:
            board_cell_successor = board.get_value_for_coordinates(
                x=cell.x,
                y=cell.y
            )
            board.set_board_cell_filled_by_object(
                x=cell.x,
                y=cell.y,
                filled_object=board_cell_successor
            )
            new_cells_objects.append(board_cell_successor)
        shape.save_filled_board_cells(new_cells_objects)
        shape.set_start_x(shape_start_x)
        shape.set_start_y(shape_start_y)


class MoveClockwiseCounter(MoveRotation):
    letter = 's'
    description = "Move clockwise counter"

    @classmethod
    def move(self, board, shape):
        shape_start_x, shape_start_y = shape.start_x, shape.start_y
        shape.rotate_clockwise_counter()

        new_cells = []

        for y, row in enumerate(shape.current_shape.current_shape_array):
            for x, value in enumerate(row):
                if value == 1:
                    new_cells.append(
                        Coordinates(x=shape_start_x + x, y=shape_start_y + y)
                    )

        previous_cells = shape.get_cells()
        for board_cell in previous_cells:
            board_cell.remove_filled_by_object()

        new_cells_objects = []
        for cell in new_cells:
            board_cell_successor = board.get_value_for_coordinates(
                x=cell.x,
                y=cell.y
            )
            board.set_board_cell_filled_by_object(
                x=cell.x,
                y=cell.y,
                filled_object=board_cell_successor
            )
            new_cells_objects.append(board_cell_successor)
        shape.save_filled_board_cells(new_cells_objects)
        shape.set_start_x(shape_start_x)
        shape.set_start_y(shape_start_y)


class MoveDown(Move):
    """
    Move that is performed after each move
    We can also move like that manually to speed up game flow.
    """
    letter = 'x'
    description = "Move down"

    @classmethod
    def move(cls, board, shape):
        new_start_x, new_start_y = shape.start_x, shape.start_y + 1

        cells_order = shape.get_cells_from_bottom_order()
        new_cells = []
        for board_cell in cells_order:
            board_cell_successor_x = board_cell.x
            board_cell_successor_y = board_cell.y + 1
            board_cell_successor = board.get_value_for_coordinates(
                x=board_cell_successor_x,
                y=board_cell_successor_y
            )
            board.set_board_cell_filled_by_object(
                x=board_cell_successor_x,
                y=board_cell_successor_y,
                filled_object=board_cell_successor
            )
            new_cells.append(board_cell_successor)
            board_cell.remove_filled_by_object()
        shape.save_filled_board_cells(new_cells)
        shape.set_start_x(new_start_x)
        shape.set_start_y(new_start_y)

    @classmethod
    def can_move(cls, board, shape):
        size_x = shape.get_size_x()
        size_y = shape.get_size_y()
        shape_y_position = shape.start_y + size_y

        if shape_y_position > board.size_board:
            return False

        for x in range(size_x):
            if board.get_value_for_coordinates(
                x=x+shape.start_x,
                y=shape_y_position
            ).is_filled():
                return False

        return True


MOVES = [MoveLeft, MoveRight, MoveClockwise, MoveClockwiseCounter]
MOVES_DICT = {
    MoveLeft.letter: MoveLeft,
    MoveRight.letter: MoveRight,
    MoveClockwise.letter: MoveClockwise,
    MoveClockwiseCounter.letter: MoveClockwiseCounter,
    MoveDown.letter: MoveDown,
}
MOVE_LETTERS_CHOICES = list(MOVES_DICT.keys())
MOVE_LETTERS_CHOICES_WITH_DESCRIPTION = {letter: move.description for letter, move in MOVES_DICT.items()}