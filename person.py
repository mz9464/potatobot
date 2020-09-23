"""
file: person.py
author: Misty Zheng
description: holds the person class and helper functions
"""

class Person:
    """ Person class that contains a user name, id, and reputation """
    def __init__(self, name, id, rep=0):
        self.name = name
        self.id = id
        self.rep = rep

    """ Changes a Person's reputation by a certain amount """
    def change_rep(self, rep=0):
        self.rep += rep

    """ Returns a Person's id """
    def get_id(self):
        return self.id

    """ Returns a Person's reputation """
    def get_rep(self):
        return self.rep
