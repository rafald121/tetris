import random

import numpy as np


class Shape:
    shape_array = None


class ShapeLine(Shape):
    shape_array = [[1, 1, 1, 1]]

    @classmethod
    def get_shape(cls):
        return cls.shape_array


class ShapeL(Shape):
    shape_array = [
        [1, 0],
        [1, 0],
        [1, 1]
    ]

    @classmethod
    def get_shape(cls):
        return cls.shape_array


class ShapeLReversed(Shape):
    shape_array = [
        [0, 1],
        [0, 1],
        [1, 1]
    ]

    @classmethod
    def get_shape(cls):
        return cls.shape_array


class ShapeLightening(Shape):
    shape_array = [
        [0, 1],
        [1, 1],
        [1, 0]
    ]

    @classmethod
    def get_shape(cls):
        return cls.shape_array


class ShapeSquare(Shape):
    shape_array = [
        [1, 1],
        [1, 1],
    ]

    @classmethod
    def get_shape(cls):
        return cls.shape_array


shapes = [
    ShapeLine, ShapeL, ShapeLReversed, ShapeLightening, ShapeSquare
]


class Shapes(list):

    def __init__(self):
        super().__init__()
        self.initialize_shapes()

    def initialize_shapes(self):
        for shape in shapes:
            self.append(ShapeElement(shape.shape_array))

    def get_random_shape(self) -> 'ShapeElement':
        return random.choice(self)

    def get_random_shapes(self):
        random_indexes = random.sample(range(0, 5), 5)
        return [self[index] for index in random_indexes]


class ShapeElement:

    def __init__(self, shape_matrix):
        self.init_shape_matrix = shape_matrix
        self.current_shape = shape_matrix
        self.current_shape_array = np.array(shape_matrix)

    def get_size(self):
        return self.get_size_y(), self.get_size_x()

    def get_size_y(self):
        return self.current_shape_array.shape[0]

    def get_size_x(self):
        return self.current_shape_array.shape[1]

    def rotate_clockwise_counter(self):
        rotated_array = np.rot90(self.current_shape.current_shape_array, 1)
        self.current_shape.current_shape_array = rotated_array

    def rotate_clockwise(self):
        rotated_array = np.rot90(self.current_shape.current_shape_array, 3)
        self.current_shape.current_shape_array = rotated_array

    def __str__(self):
        return str(self.current_shape_array)

