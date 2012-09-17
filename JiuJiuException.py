#!/usr/bin/env python
class UserWantRestart(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value

class ErrorToUser(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value
