#!/usr/bin/env python3
"""Demonstrates mixins using a Dragon class."""


class SwimMixin:
    """Provide swimming behavior."""

    def swim(self):
        """Print a swimming message."""
        print("The creature swims!")


class FlyMixin:
    """Provide flying behavior."""

    def fly(self):
        """Print a flying message."""
        print("The creature flies!")


class Dragon(SwimMixin, FlyMixin):
    """Represent a dragon that can swim and fly."""

    def roar(self):
        """Print a roaring message."""
        print("The dragon roars!")
