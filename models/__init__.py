#!/usr/bin/python3
"""__init__  to create a unique FileStorage instance for your application"""
import os

storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from .engine.db_storage import DBStorage

    storage = DBStorage()
    storage.reload()

else:
    from .engine.file_storage import FileStorage

    storage = FileStorage()
    storage.reload()
