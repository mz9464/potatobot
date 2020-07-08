"""
file: person.py
author: Misty Zheng
description: holds the person class and helper functions
"""

class Person:
    """ Person class that contains a user name and reputation """
    def __init__(self, name, rep=0):
        self.name = name
        self.rep = rep

    def get_name(self):
        return self.name