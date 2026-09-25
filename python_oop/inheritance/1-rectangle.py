#!/usr/bin/env python3
"""Defines a Rectangle class that inherits from BaseGeometry."""

from base_geometry import BaseGeometry


class Rectangle(BaseGeometry):
    """Represents a rectangle."""

    def __init__(self, width, height):
        """Initialize a rectangle with width and height."""
        self.integer_validator("width", width)
        self.integer_validator("height", height)

        self.__width = width
        self.__height = height