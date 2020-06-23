#!/usr/bin/python3

"""
Custom game-related exceptions

"""

class NoCardError(Exception):
    """Exception raised when there are no cards in deck"""

class NumPlayerError(Exception):
    """Exception raised when there are too little/many players"""

class TimeoutExpiredError(Exception):
    """Exception raised when time expires on a user stdin prompt"""
