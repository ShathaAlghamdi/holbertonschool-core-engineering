#!/usr/bin/env python3
"""Demonstrates multiple inheritance with a FlyingFish class."""


class Fish:
    """Represents a fish."""

    def swim(self):
        """Print the swimming behavior."""
        print("The fish is swimming")

    def habitat(self):
        """Print the fish habitat."""
        print("The fish lives in water")


class Bird:
    """Represents a bird."""

    def fly(self):
        """Print the flying behavior."""
        print("The bird is flying")

    def habitat(self):
        """Print the bird habitat."""
        print("The bird lives in the sky")


class FlyingFish(Fish, Bird):
    """Represents a flying fish."""

    def fly(self):
        """Print the flying fish's flying behavior."""
        print("The flying fish is soaring!")

    def swim(self):
        """Print the flying fish's swimming behavior."""
        print("The flying fish is swimming!")

    def habitat(self):
        """Print the flying fish's habitat."""
        print("The flying fish lives both in water and the sky!")
