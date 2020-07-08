"""
file: person.py
author: Misty Zheng
description: holds the person class
"""

class Person:
    """ Person class that contains a user id and reputation """
    def __init__(self, id, rep = 0):
        self.id = id
        self.rep = rep
