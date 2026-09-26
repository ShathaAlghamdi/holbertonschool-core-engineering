#!/usr/bin/env python3
"""Defines a VerboseList class extending the built-in list."""


class VerboseList(list):
    """A list that prints notifications when modified."""

    def append(self, item):
        """Append an item and print a notification."""
        super().append(item)
        print("Added {} to the list.".format(item))

    def extend(self, iterable):
        """Extend the list and print the number of added items."""
        items = list(iterable)
        super().extend(items)
        print("Extended the list with {} items.".format(len(items)))

    def remove(self, item):
        """Remove an item and print a notification."""
        print("Removed {} from the list.".format(item))
        super().remove(item)

    def pop(self, index=-1):
        """Pop an item and print a notification."""
        item = self[index]
        print("Popped {} from the list.".format(item))
        return super().pop(index)
