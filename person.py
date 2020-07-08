"""
file: person.py
author: Misty Zheng
description: holds the person class
"""

class Person:
    """ Person class that contains a user name and reputation """
    def __init__(self, name, rep=0):
        self.name = name
        self.rep = rep
