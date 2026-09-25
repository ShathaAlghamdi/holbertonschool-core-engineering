#!/usr/bin/env python3
"""Defines a Square class with size and position."""


class Square:
    """Represents a square."""

    def __init__(self, size=0, position=(0, 0)):
        """Initialize a square with size and position."""
        self.size = size
        self.position = position

    @property
    def size(self):
        """Return the size of the square."""
        return self.__size

    @size.setter
    def size(self, value):
        """Set and validate the size of the square."""
        if type(value) is not int:
            raise TypeError("size must be an integer")

        if value < 0:
            raise ValueError("size must be >= 0")

        self.__size = value

    @property
    def position(self):
        """Return the position of the square."""
        return self.__position

    @position.setter
    def position(self, value):
        """Set and validate the position of the square."""
        if (
            type(value) is not tuple
            or len(value) != 2
            or type(value[0]) is not int
            or type(value[1]) is not int
            or value[0] < 0
            or value[1] < 0
        ):
            raise TypeError(
                "position must be a tuple of 2 positive integers"
            )

        self.__position = value

    def area(self):
        """Return the area of the square."""
        return self.__size ** 2

    def my_print(self):
        """Print the square using its position."""
        print(self)

    def __str__(self):
        """Return the printable representation of the square."""
        if self.__size == 0:
            return ""

        result = "\n" * self.__position[1]

        for i in range(self.__size):
            result += " " * self.__position[0]
            result += "#" * self.__size

            if i < self.__size - 1:
                result += "\n"

        return result
