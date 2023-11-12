#!/usr/bin/python3
'''"Models" folder init module
    Creates a unique FileStorage instance 'storage' for the AirBnB clone app
'''
from .engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
