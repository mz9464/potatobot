"""
file: person.py
author: Misty Zheng
description: holds the person class and helper functions
"""

class Person:
    """ Person class that contains a user name, id, and reputation """
    def __init__(self, name, rep=0):
        self.name = name
        self.id = id
        self.rep = rep

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def change_rep(self, rep=0):
        self.rep = rep