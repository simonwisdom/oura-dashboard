import sys
import os

# This sets the path for the Flask app, which needs to be importable by the WSGI server
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

# Import the Flask app instance
from run import app as application
