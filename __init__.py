# src/__init__.py

# This file can be empty, or it can contain package-level initialization code.

# 1. Empty __init__.py:

# The most common use case for __init__.py is simply to mark a directory as a Python package.  
# An empty __init__.py file is perfectly valid and sufficient for this purpose.  This tells Python
# that the 'src' directory should be treated as a package, allowing you to import modules
# from it using dot notation (e.g., `from src.face_recognition_system import FaceRecognitionSystem`).

# 2. Package-Level Initialization (Optional):

#  You *can* put code in __init__.py, and it will be executed when the package (or any module within it) is imported.
#  This is generally used for:

#   a) Package-Level Constants: Define constants that are relevant to the entire package.
#   b) Submodule Imports: Make submodules or specific functions/classes more easily accessible.
#   c) Package-Level Setup: Perform one-time setup tasks for the package.
#   d) Namespace Management: Control what is exposed by the package.

# Here are some examples of what you *could* put in __init__.py, but *shouldn't* in this specific project
# because it's better handled in separate modules (config.py, database.py) as we already did.  I'm showing
# these examples for completeness, to illustrate what __init__.py *can* do, but I'll then show
# the recommended, cleaner approach for our face recognition project.

# --- Examples (NOT recommended for this project, but illustrative) ---

# Example 2a: Package-Level Constants (Better to put in config.py)
# __init__.py
# DEFAULT_TOLERANCE = 0.6
# DATABASE_FILENAME = "faces.db"

# Then, in other modules:
# from src import DEFAULT_TOLERANCE

# Example 2b: Submodule Imports (Better handled with explicit imports)
# __init__.py
# from .face_recognition_system import FaceRecognitionSystem
# from .utils import load_image

# Then, you could import like this (but it's less clear where things come from):
# from src import FaceRecognitionSystem, load_image

# Example 2c: Package-Level Setup (Better to handle in database.py)
# __init__.py
# import sqlite3
#
# def _initialize_database():
#     conn = sqlite3.connect("faces.db") # Don't hardcode the path here!  Use config.py
#     # ... create tables if they don't exist ...
#     conn.close()
#
# _initialize_database()  # Call the setup function when the package is imported.

# Example 2d: Namespace Management (Usually not needed for simple projects)
# __init__.py
# from .face_recognition_system import FaceRecognitionSystem
#
# __all__ = ["FaceRecognitionSystem"]  # Only FaceRecognitionSystem is exposed when using 'from src import *'

# --- Recommended Approach for the Face Recognition Project ---

# src/__init__.py (Keep it simple!)

# Best Practice:  Leave __init__.py EMPTY for this project.

# The best practice for this project is to keep `src/__init__.py` EMPTY.  We have already:
#
# *   Put configuration settings in `config.py`.
# *   Put database initialization in `database.py`.
# *   Used explicit imports in our modules (e.g., `from src.face_recognition_system import FaceRecognitionSystem`).
#
# This keeps the code clean, modular, and easy to understand.  An empty `__init__.py` file is perfectly valid
# and is the standard way to indicate that a directory is a Python package.