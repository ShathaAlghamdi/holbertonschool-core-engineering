#!/usr/bin/env python3
"""Defines a Square class that inherits from Rectangle."""

Rectangle = __import__('2-rectangle').Rectangle


class Square(Rectangle):
    """Represents a square."""

    def __init__(self, size):
        """Initialize a square with a validated size."""
        self.integer_validator("size", size)

        self.__size = size

        super().__init__(size, size)

    def area(self):
        """Return the area of the square."""
        return self.__size ** 2

    def __str__(self):
        """Return the string representation of the square."""
        return "[Square] {}/{}".format(
            self.__size, self.__size
        )
